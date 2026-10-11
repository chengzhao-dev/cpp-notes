#!/usr/bin/env python3
"""check_content_budget.py - content 篇幅的 token 预算校验。

口径和限额均与知识文件 cpp-quarto-chapter-structure-v1「分层上限」一致（两处必须同步）：
正文、标题、列表、表格、Callout 与链接锚文本计入 token；frontmatter、
链接 URL、代码围栏、{mermaid} 图与 {python} 可执行单元不计入，改由
分层的行数上限与注释约束。同时扫描正文全角分号（WARN，不判失败）。
与姊妹仓库 cpp-board-games 的 verify_content.py 同口径；普通代码块
按本仓 code-style.md 保留 40 行。
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTENT_GLOBS = ["content/**/*.qmd", "index.qmd"]

CJK_RE = re.compile(r"[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef\u3000-\u303f]")
FILE_TOKENS = 5000
INTRO_TOKENS = 400
H2_TOKENS = 1800
H3_TOKENS = 600
H3_COUNT = 4
# 普通代码块 40 行是本仓差异（code-style.md）；图表与可执行单元限额与
# board-games 相同。
BLOCK_LINES = 40
MERMAID_LINES = 40
PY_CELL_LINES = 30
PARA_TOKENS = 220
# 节导语与引用块限额（与知识「分层上限」同口径）：## 节导语
# 120 token 且 ≤2 句，### 节导语 80 token 且 ≤1 句，单个 > 引用块
# 80 token。节导语指从标题之后到首个代码块/列表/表格/引用/盒子之前
# 的连续正文；空行分段不结束导语。
LEAD_H2_TOKENS = 120
LEAD_H2_SENTENCES = 2
LEAD_H3_TOKENS = 80
LEAD_H3_SENTENCES = 1
QUOTE_TOKENS = 80
SENTENCE_END_RE = re.compile(r"[。！？]")
CODE_LANGS = {"cpp", "cmake", "bash", "sh", "python", "jsonc"}

# Markdown 链接在预算计数前剥离 URL：URL 是机器寻址串，读者扫读时整体
# 跳过；锚文本保留照常计数（口径见标识 cpp-quarto-chapter-structure-v1）。
LINK_URL_RES = [
    re.compile(r"\]\([^)\s]*https?://[^)\s]*\)"),
    re.compile(r"<https?://[^>\s]+>"),
]


def strip_link_urls(text):
    for pattern in LINK_URL_RES:
        text = pattern.sub("]()", text)
    return text


def estimate_tokens(text):
    """按 cpp-quarto-chapter-structure-v1 口径估算 token 数：CJK×1.5 + 其他÷4。"""
    cjk = len(CJK_RE.findall(text))
    return int(cjk * 1.5 + (len(text) - cjk) / 4)


def count_sentences(text):
    """按句终标点估算句数；句内逗号、分号不另起句。"""
    return len(SENTENCE_END_RE.findall(text))


def check_file_budget(path):
    """按篇幅预算核对单个 qmd，返回错误明细列表。

    逐行归类到 (二级标题, 三级标题) 桶：二级为 None 表示无标题引言，
    三级为 None 表示 ## 直接内容。token 计数只覆盖正文（标题、列表、
    表格、Callout 与锚文本）；代码围栏、{mermaid} 图与 {python} 可执行
    单元不计 token，改由各自的行数上限与注释约束管住。另核节导语
    （标题后、首个代码块/列表/表格/引用/盒子前的连续正文）与单个 >
    引用块的 token 与句数限额；着陆页跳过。
    """
    rel = str(path.relative_to(REPO_ROOT))
    errors = []
    lead_errors = []
    quote_errors = []
    raw = path.read_text(encoding="utf-8").splitlines()
    offset = 0
    if raw and raw[0].strip() == "---":
        for i in range(1, len(raw)):
            if raw[i].strip() == "---":
                offset = i + 1
                break
    lines = raw[offset:]

    tokens = {}  # (二级标题, 三级标题) -> 估算 token
    h3_count = {}  # 二级标题 -> ### 数量
    fence_lang = None
    fence_lineno = 0
    fence_limit = BLOCK_LINES
    fence_lines = 0
    h2 = None
    h3 = None
    para_start = None
    para_text = []
    lead_start = None  # 当前节导语首行号
    lead_text = []
    lead_open = False
    lead_is_h3 = False
    quote_start = None  # 当前引用块首行号
    quote_text = []

    def flush_para():
        """正文段落超限时报错；无未结算段落时不动作。"""
        nonlocal para_start, para_text
        if para_start is not None and para_text:
            size = estimate_tokens(strip_link_urls("".join(para_text)))
            if size > PARA_TOKENS:
                errors.append(
                    f"{rel}:{para_start}: 正文段落约 {size} token，"
                    f"超过 {PARA_TOKENS}（见标识 cpp-quarto-chapter-structure-v1）"
                )
        para_start = None
        para_text = []

    def flush_lead():
        """节导语超 token 或超句数时报错；导语未开启或为空时不动作。"""
        nonlocal lead_start, lead_text, lead_open
        if lead_open and lead_text:
            body = strip_link_urls("".join(lead_text))
            size = estimate_tokens(body)
            sentences = count_sentences(body)
            if lead_is_h3:
                limit, slimit, kind = (
                    LEAD_H3_TOKENS, LEAD_H3_SENTENCES, "三级标题")
            else:
                limit, slimit, kind = (
                    LEAD_H2_TOKENS, LEAD_H2_SENTENCES, "二级标题")
            if size > limit or sentences > slimit:
                lead_errors.append(
                    f"{rel}:{lead_start}: {kind}节导语约 {size} token / "
                    f"{sentences} 句，超过 {limit} token / {slimit} 句"
                    f"（见标识 cpp-quarto-chapter-structure-v1）"
                )
        lead_start = None
        lead_text = []
        lead_open = False

    def flush_quote():
        """引用块超 token 时报错；无未结算引用块时不动作。"""
        nonlocal quote_start, quote_text
        if quote_start is not None and quote_text:
            size = estimate_tokens(strip_link_urls("".join(quote_text)))
            if size > QUOTE_TOKENS:
                quote_errors.append(
                    f"{rel}:{quote_start}: 引用块约 {size} token，"
                    f"超过 {QUOTE_TOKENS}（见标识 cpp-quarto-chapter-structure-v1）"
                )
        quote_start = None
        quote_text = []

    def add_token(text):
        key = (h2, h3)
        tokens[key] = tokens.get(key, 0) + estimate_tokens(strip_link_urls(text))

    for i, line in enumerate(lines):
        lineno = offset + i + 1
        if fence_lang is not None:
            if line.startswith("```"):
                flush_para()
                label = f"{rel}:{fence_lineno}"
                if fence_lines > fence_limit:
                    errors.append(
                        f"{label}: 代码块 {fence_lines} 行，超过 {fence_limit} 行"
                    )
                fence_lang = None
                continue
            fence_lines += 1
            continue
        if line.startswith("```"):
            flush_para()
            flush_lead()
            flush_quote()
            after = line[3:].strip()
            match = re.match(r"\{?\.?(\w+)", after)
            fence_lang = (match.group(1) if match else "").lower()
            fence_lineno = lineno
            # {mermaid} 是图表围栏，{python} 可执行单元是坐标图的调用入口：
            # 两类都只受自身行数上限约束，不参与 token 计数。
            # mermaid 必须先于可执行单元判定，{mermaid} 同样以 { 开头。
            if fence_lang == "mermaid":
                fence_limit = MERMAID_LINES
            elif after.startswith("{") and not after.startswith("{."):
                fence_limit = PY_CELL_LINES
            else:
                fence_limit = BLOCK_LINES
            fence_lines = 0
            continue
        if line.startswith("### ") and h2 is not None:
            flush_para()
            flush_lead()
            flush_quote()
            h3 = line[4:].strip()
            h3_count[h2] = h3_count.get(h2, 0) + 1
            add_token(line)
            lead_start = lineno
            lead_text = []
            lead_open = True
            lead_is_h3 = True
            continue
        if line.startswith("## "):
            flush_para()
            flush_lead()
            flush_quote()
            h2 = line[3:].strip()
            h3 = None
            add_token(line)
            lead_start = lineno
            lead_text = []
            lead_open = True
            lead_is_h3 = False
            continue
        # 标题、列表、表格、div 标记与引用行是段落边界；其余连续文本行
        # 累计为段落，口径见标识 cpp-quarto-chapter-structure-v1 的知识文件。
        stripped = line.strip()
        is_prose = (
            bool(stripped)
            and not stripped.startswith(("|", ">", ":::"))
            and not line.startswith("#")
            and not re.match(r"^\s*[-*+]\s", line)
            and not re.match(r"^\s*\d+[.、)]\s", line)
        )
        if is_prose:
            if para_start is None:
                para_start = lineno
            para_text.append(line)
            if lead_open:
                lead_text.append(line)
        else:
            flush_para()
            if stripped.startswith(">"):
                # 引用行结束节导语，并累计到当前引用块。
                flush_lead()
                if quote_start is None:
                    quote_start = lineno
                quote_text.append(stripped.lstrip(">").strip())
            else:
                flush_quote()
                if stripped:
                    # 空行只分段不结束导语；列表、表格与盒子结束导语。
                    flush_lead()
        add_token(line)

    flush_para()
    flush_lead()
    flush_quote()

    # index.qmd 是着陆页：短引言 + 卡片网格不是章节引言，只核对整章
    # 总量与代码块限额，不做引言与分节限额。
    is_landing = path.name == "index.qmd"
    chapter = not is_landing

    if chapter:
        errors.extend(lead_errors)
        errors.extend(quote_errors)
    intro = tokens.get((None, None), 0) if chapter else 0
    if intro > INTRO_TOKENS:
        errors.append(f"{rel}: 引言约 {intro} token，超过 {INTRO_TOKENS}")
    h2_totals = {}
    for (h2_key, h3_key), value in tokens.items():
        if h2_key is None or not chapter:
            continue
        h2_totals[h2_key] = h2_totals.get(h2_key, 0) + value
        if h3_key is not None and value > H3_TOKENS:
            errors.append(f"{rel}: 「{h3_key}」约 {value} token，超过 {H3_TOKENS}")
    for h2_key, value in h2_totals.items():
        if value > H2_TOKENS:
            errors.append(f"{rel}: 「{h2_key}」共约 {value} token，超过 {H2_TOKENS}")
    for h2_key, count in h3_count.items():
        if count > H3_COUNT:
            errors.append(
                f"{rel}: 「{h2_key}」下 {count} 个三级标题，超过 {H3_COUNT} 个"
            )
    total = sum(tokens.values())
    if total > FILE_TOKENS:
        errors.append(f"{rel}: 全章约 {total} token，超过 {FILE_TOKENS}")
    return errors


def find_prose_semicolon_warnings(path):
    """正文（排除 frontmatter 与围栏）出现全角分号时记 WARN。

    口径见 writing-quarto 技能 references/zh/writing-principles.md
    「句子要短，术语要稳」：正文不用分号；删掉任一分句后中心仍成立的
    多中心句，其改写对照见知识 cpp-quarto-chinese-style-v1。只提示不判
    失败，与姊妹仓库 verify_content.py 的同项 WARN 同口径。
    """
    warnings = []
    lines = path.read_text(encoding="utf-8").splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    in_fence = False
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and "；" in line:
            warnings.append(f"{path.relative_to(REPO_ROOT)}:{i + 1}")
    return warnings


def main():
    files = []
    for pattern in CONTENT_GLOBS:
        files.extend(sorted(REPO_ROOT.glob(pattern)))
    errors = []
    warnings = []
    for path in files:
        errors.extend(check_file_budget(path))
        warnings.extend(find_prose_semicolon_warnings(path))
    if warnings:
        print(
            "WARN 正文全角分号（疑似多中心句或分号堆叠，不判失败；"
            "对照见知识 cpp-quarto-chinese-style-v1）："
        )
        for item in warnings:
            print(f"  {item}")
    if errors:
        for item in errors:
            print(item)
        print(
            f"FAIL content-budget（{len(files)} 个文档，{len(errors)} 处超限）"
        )
        raise SystemExit(1)
    print(f"PASS content-budget（{len(files)} 个文档）")


if __name__ == "__main__":
    main()
