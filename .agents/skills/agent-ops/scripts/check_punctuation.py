#!/usr/bin/env python3
"""检查中文正文是否使用了分号「；」。

为什么需要它：分号在中文技术文档里没有稳定的使用习惯，读者容易把它当成句子结束，
也会因为前后分句同等重要而判断不出主线。规则见 `writing-principles.md` 第 9 条与
`knowledge/quarto-docs/writing/chinese-style-cases.md`「分号与句长」。

只扫描正文：跳过代码围栏内部、行内代码、URL 和被引号引用起来的标点本身，
因此代码语法里的半角分号和「正文不用分号“；”」这类规则表述不受影响。

用法：check_punctuation.py [--verbose] [--strict]
退出码：0 = 通过，1 = --strict 下发现分号。默认把命中作为 NOTICE 输出并以 0 退出。
"""

from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[4]
SKIP = {".git", "_book", ".quarto", ".cache", "build", "node_modules", "temp", "__pycache__"}
DOC_EXTENSIONS = {".md", ".qmd"}
CODE_EXTENSIONS = {".py", ".sh", ".bash", ".cpp", ".cc", ".cmake", ".txt", ".yml", ".yaml"}
FENCE = re.compile(r"^\s*(?:```|~~~)")
URL = re.compile(r"https?://\S+")
COMMENT_PREFIX = {
    ".py": ("#",),
    ".sh": ("#",), ".bash": ("#",), ".txt": ("#",), ".cmake": ("#",),
    ".yml": ("#",), ".yaml": ("#",),
    ".cpp": ("//", "*", "#"), ".cc": ("//", "*", "#"),
}
SEMICOLON = "；"
MENTION = "\u201c；\u201d"  # 规则文本里引用标点本身，不算使用


def documents():
    paths = [ROOT / "README.md", ROOT / "AGENTS.md"]
    for folder in ("content", "knowledge", ".agents", "code"):
        base = ROOT / folder
        if base.is_dir():
            paths.extend(p for p in base.rglob("*") if p.is_file())
    allowed = DOC_EXTENSIONS | set(COMMENT_PREFIX)
    found = []
    for path in set(paths):
        if any(part in SKIP for part in path.parts):
            continue
        if path.suffix.lower() not in allowed:
            continue
        if path.is_file():
            found.append(path)
    return sorted(found)


def inline_ranges(line):
    """行内代码与 URL 的字符区间，这些位置照抄真实语法，不做标点检查。"""
    ranges = []
    index, length = 0, len(line)
    while index < length:
        if line[index] == "`":
            end = index
            while end < length and line[end] == "`":
                end += 1
            run = end - index
            close = line.find("`" * run, end)
            if close != -1:
                ranges.append((index, close + run))
                index = close + run
                continue
        match = URL.search(line, index)
        if match:
            ranges.append((match.start(), match.end()))
            index = match.end()
            continue
        index += 1
    return ranges


def scannable(line, suffix):
    """该行的分号是否属于正文（需要检查）。"""
    stripped = line.strip()
    if suffix in DOC_EXTENSIONS:
        return True
    prefixes = COMMENT_PREFIX.get(suffix, ())
    return bool(prefixes) and stripped.startswith(prefixes)


def find_hits(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    hits = []
    in_fence = False
    in_docstring = False
    suffix = path.suffix.lower()
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if suffix == ".py":
            count = line.count('"""') + line.count("'''")
            editable = in_docstring or SEMICOLON in line and line.strip().startswith("#")
            in_docstring = (in_docstring + count) % 2 == 1
        else:
            editable = scannable(line, suffix)
        if not editable or SEMICOLON not in line:
            continue
        ranges = inline_ranges(line)
        for index, char in enumerate(line):
            if char != SEMICOLON:
                continue
            if line[index - 1:index + 2] == MENTION:
                continue
            if any(start <= index < end for start, end in ranges):
                continue
            hits.append((number, line.strip()))
            break
    return hits


def main():
    parser = argparse.ArgumentParser(description="检查中文正文分号")
    parser.add_argument("--verbose", action="store_true", help="展开全部命中")
    parser.add_argument("--strict", action="store_true", help="把命中视为失败")
    args = parser.parse_args()

    paths = documents()
    findings = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        for number, snippet in find_hits(path):
            findings.append(f"{rel}:{number}: 正文不使用分号“；”，并列分句改用逗号，独立分句拆成两句")
    for finding in findings:
        print("NOTICE punctuation " + finding)
    shown = findings if args.verbose else findings[:10]
    if findings and args.strict:
        print(f"FAIL punctuation  {len(findings)} 处正文分号")
        for line in shown:
            print("  " + line)
        return 1
    detail = f"（非 strict，{len(findings)} 处记为 NOTICE）" if findings else ""
    print(f"PASS punctuation  扫描 {len(paths)} 个文件，正文无分号要求违规{detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
