#!/usr/bin/env python3
#===------------------------------------------------------------------------===#
# check_forbidden_terms.py - content 侧压缩黑话与语气禁词检查
#
# 对 content/**/*.qmd 与根 index.qmd 扫描禁用词与禁用句式。禁词是回潮网，
# 不是写作方法：正文按 writing-quarto 的 references 与知识文件写作，本脚本
# 只防止已删掉的措辞回潮。在仓库根目录执行；优先用根目录 config.toml 的
# python 完整路径启动。只用标准库；发现即退出码 1。
#
# 范围参数：
#   --paths ...  只检查指定 qmd 文件或目录（相对仓库根）
#   --changed    只检查 git 工作区改动的 qmd（相对 HEAD）
#===------------------------------------------------------------------------===#

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

#===------------------------------------------------------------------------===#
# 检查配置
#===------------------------------------------------------------------------===#

# 压缩隐喻与电报体（对照见标识 cpp-quarto-chinese-style-v1 的知识文件
# 「压缩黑话与电报体」）：读者正文写可观察对象与完整主谓句。
FORBIDDEN_TERMS = [
    "契约链", "谁消费", "消费", "契约",
    "状态外壳", "地基", "执行纪律", "闭环", "落地",
    "CLI 打印",
    # 语气与语域：口语讲义腔、命令口与倒装强调。
    "读懂", "务必", "严禁", "千万不要", "千万别",
    "动手前", "弄清", "咱们", "搞定", "别慌",
    "本章规划", "落点是", "跑通", "这正是", "容易混淆",
    # 头文件指称必须点名具体对象（文件名、include/ 路径、调用方），
    # 或写全「库对外头文件」；省略缩略与「公共」前缀堆叠停用
    # （与 cpp-board-games 同一口径，规则见标识 bg-terminology-v1）。
    "公共头", "公共值类型",
]

# 词表表达不了的句式用正则：渐进披露元叙述（写作策略不念给读者听）。
FORBIDDEN_PATTERNS = [
    (r"语法细节留到", "渐进披露元叙述（直接陈述对象和结果）"),
    (r"真正用到时再", "渐进披露元叙述（直接陈述对象和结果）"),
    (r"本章只需认清", "渐进披露元叙述（直接陈述对象和结果）"),
    # 过程节标题承载回顾职责（规则见标识 cpp-quarto-chapter-structure-v1）：
    # 「本章做到哪、后续章接什么」只写在 ## 本章回顾。
    (r"^#{2,4}\s+.*实现边界", "过程节标题含「实现边界」（并入本章回顾）"),
    # 目录树行尾注释是名词性职责短语（规则见标识 cpp-quarto-qmd-element-cases-v1）：
    # 不用全角冒号挂解释。
    (r"^.*[├└]─.*：", "目录树行尾注释含全角冒号（改名词性短语）"),
    # filename 是短显示名字符串（规则见标识 cpp-quarto-qmd-element-cases-v1）：
    # 不塞 Markdown 链接，完整路径靠同节正文链接提供。
    (r'filename="[^"]*\]\(', "filename 含 Markdown 链接（只写短名）"),
    # 突兀跨仓依据句（规则见 chapter-writing.md「跨仓外链」、
    # cpp-quarto-chinese-style-v1「突兀跨仓依据句」）：语言约定不挂
    # 「依据见 / 机制见 …」+ cpp-board-games。
    (r"(?:写法)?依据见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除或改尾置若要系统阅读）"),
    (r"(?:语言)?机制见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除或改尾置若要系统阅读）"),
    (r"选型见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除或改尾置若要系统阅读）"),
    (r"承诺见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除或改尾置若要系统阅读）"),
    (r"用法见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除或改尾置若要系统阅读）"),
    (r"陷阱见.{0,40}(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（删除选型链）"),
    (r"完整讲解在\s*(?:cpp-board-games|board-games)",
     "突兀跨仓依据句（改本仓讲清或删）"),
    # 目录树行尾注释写完整职责短语（与 cpp-board-games 同一口径）：
    # 头文件目录注释写「库对外头文件」，不写「公开头文件」。
    (r"#\s*公开头文件", "目录树注释改「库对外头文件」"),
    # 课堂类比（与 cpp-board-games 同一口径，规则见 chapter-writing.md）：
    # 坐标系等工程对象只写程序事实与可观察行为，不借数学课对照。
    (r"数学课", "课堂类比（改写为工程对象与可观察行为）"),
    (r"平面直角坐标", "课堂类比（改写为工程对象与可观察行为）"),
]
FORBIDDEN_RES = [(re.compile(pattern), label) for pattern, label in FORBIDDEN_PATTERNS]

#===------------------------------------------------------------------------===#
# 上下文相关检查配置：完整符号与 Mermaid 窄屏方向
#===------------------------------------------------------------------------===#

# 正文裸 `Status`（与 board-games 同一规则）：同文件出现 GameStatus 时，
# 正文不得把枚举类型简写成 `Status`，须写完整符号 `GameStatus` 或
# `GameState::Status`；代码围栏内照抄源码不受限。
BARE_STATUS_RE = re.compile(r"(?<![:\w])`Status`")

# 整行仅为 Markdown 链接（与 board-games 同一规则）：来源链接要嵌进
# 同节导语句子，禁止单独成行贴在代码围栏上方。
BARE_LINK_LINE_RE = re.compile(r"^\[[^\]]*\]\([^)]*\)$")

# `##` 标题汉字数上限（WARN，与 board-games 同一规则；见标识
# cpp-quarto-chapter-structure-v1 的知识文件「标题字数硬限」）：仅统计汉字。
H2_HAN_LIMIT = 10
HAN_RE = re.compile(r"[\u4e00-\u9fff]")

# {mermaid} 图方向（规则见标识 cpp-mermaid-conventions-v1 的知识文件）：
# flowchart/graph LR 且节点标签数达到阈值时挤爆窄屏视口，改 TB 或拆图。
MERMAID_NODE_RE = re.compile(r'\["[^"]*"\]')
MERMAID_LR_NODE_LIMIT = 5
MERMAID_DIR_RE = re.compile(r"\b(?:flowchart|graph)\s+LR\b")

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTENT_GLOBS = ["content/**/*.qmd", "index.qmd"]
MIN_PYTHON = (3, 11)

#===------------------------------------------------------------------------===#
# 受控解释器（与 board-games 同款约定：只认 config.toml，不回退 PATH）
#===------------------------------------------------------------------------===#

def to_form(path: Path, form: str) -> str:
    """在 Windows 与 WSL 路径形态间转换：D:/a/b <-> /mnt/d/a/b。"""
    text = str(path).replace("\\", "/")
    drive = re.match(r"^([A-Za-z]):/(.*)$", text)
    mount = re.match(r"^/mnt/([A-Za-z])/(.*)$", text)
    if form == "posix" and drive:
        return f"/mnt/{drive.group(1).lower()}/{drive.group(2)}"
    if form == "win" and mount:
        return f"{mount.group(1).upper()}:/{mount.group(2)}"
    return text


def reexec_under_configured_python() -> None:
    """统一用 config.toml 的 python 运行本脚本；配置缺失或不可用立即失败。"""
    try:
        import tomllib
    except ImportError:
        print("失败  启动脚本需要 Python >= 3.11（tomllib）；请更新 config.toml 的解释器")
        raise SystemExit(1)
    try:
        config = tomllib.loads((REPO_ROOT / "config.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        print("失败  无法读取根目录 config.toml；请修复 python 字段")
        raise SystemExit(1)
    configured = str(config.get("python") or "").strip()
    if not configured:
        print("失败  config.toml 未配置 python 字段")
        raise SystemExit(1)

    if re.match(r"^[A-Za-z]:/", configured):
        target_form = "win"
    elif configured.startswith("/mnt/"):
        target_form = "posix"
    else:
        target_form = "win" if os.name == "nt" else "posix"

    if target_form == "posix" and os.name == "nt":
        print("失败  config.toml 的 python 是 WSL 路径；请在 WSL 中运行本脚本")
        raise SystemExit(1)

    os_path = to_form(Path(configured), "posix" if os.name == "posix" else "win")
    if not Path(os_path).is_file():
        print(f"失败  config.toml 的解释器不存在: {configured}")
        raise SystemExit(1)
    if os.path.normcase(os_path) == os.path.normcase(sys.executable):
        return
    script_arg = to_form(Path(__file__).resolve(), target_form)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    os.execve(os_path, [os_path, script_arg, *sys.argv[1:]], env)

#===------------------------------------------------------------------------===#
# 扫描
#===------------------------------------------------------------------------===#

use_color = (
    sys.stdout.isatty()
    and not os.environ.get("NO_COLOR")
    and os.environ.get("TERM") != "dumb"
)
CYAN = "\033[1;36m" if use_color else ""
RED = "\033[1;31m" if use_color else ""
RESET = "\033[0m" if use_color else ""


def resolve_qmd_paths(args):
    """返回待检查的 qmd 路径：--paths/--changed 缩小范围，默认全量。"""
    if args.paths:
        files = []
        for raw in args.paths:
            path = Path(raw)
            if not path.is_absolute():
                path = REPO_ROOT / path
            path = path.resolve()
            if REPO_ROOT.resolve() not in path.parents and path != REPO_ROOT.resolve():
                print(f"失败  --paths 路径超出仓库范围: {raw}")
                raise SystemExit(1)
            if path.is_dir():
                files.extend(sorted(path.rglob("*.qmd")))
            elif path.is_file():
                files.append(path)
            else:
                print(f"失败  --paths 路径不存在: {raw}")
                raise SystemExit(1)
        return sorted(set(files))
    if args.changed:
        proc = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z"], cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        if proc.returncode != 0:
            print(f"失败  git status 不可用：{proc.stdout.decode('utf-8', errors='replace').strip()}")
            raise SystemExit(1)
        paths, items = [], proc.stdout.decode("utf-8", errors="replace").split("\0")
        index = 0
        while index < len(items):
            item = items[index]
            if not item or len(item) < 4:
                index += 1
                continue
            status, path = item[:2], item[3:].strip('"').replace("\\", "/")
            if "R" in status or "C" in status:
                index += 1
            index += 1
            if not path.endswith(".qmd"):
                continue
            candidate = REPO_ROOT / path
            if candidate.is_file():
                paths.append(candidate)
        return sorted(set(paths))
    return sorted(
        path for pattern in CONTENT_GLOBS for path in REPO_ROOT.glob(pattern)
    )


def scan(qmd_files):
    """扫描禁用词与禁用句式，返回 [(文件, 行号, 词或标签)]。"""
    findings = []
    for path in qmd_files:
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for term in FORBIDDEN_TERMS:
                if term in line:
                    findings.append((path, lineno, term))
            for pattern, label in FORBIDDEN_RES:
                if pattern.search(line):
                    findings.append((path, lineno, label))
    return findings


def find_context_errors(path):
    """返回上下文相关错误：裸 `Status` 简称与超宽 LR 图。

    两类错误都依赖文件上下文，进不了逐行词表：裸 `Status` 只在
    同文件存在 GameStatus 时才算简称；LR 图只看节点数是否达到阈值。
    """
    errors = []
    text = path.read_text(encoding="utf-8")
    if "GameStatus" in text:
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence and BARE_STATUS_RE.search(line):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: 正文裸 `Status`，"
                    f"写完整符号 GameStatus 或 GameState::Status"
                )
    in_fence = False
    fence_lang = ""
    fence_body = []
    fence_lineno = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        if in_fence:
            if line.startswith("```"):
                if fence_lang == "mermaid" and fence_body:
                    body = "\n".join(fence_body)
                    if MERMAID_DIR_RE.search(body):
                        nodes = len(MERMAID_NODE_RE.findall(body))
                        if nodes >= MERMAID_LR_NODE_LIMIT:
                            errors.append(
                                f"{path.relative_to(REPO_ROOT)}:{fence_lineno}: "
                                f"flowchart LR 含 {nodes} 个节点（达到 "
                                f"{MERMAID_LR_NODE_LIMIT}），改 TB 或拆图"
                            )
                in_fence = False
            else:
                fence_body.append(line)
            continue
        if line.startswith("```"):
            after = line[3:].strip()
            match = re.match(r"\{?\.?(\w+)", after)
            fence_lang = (match.group(1) if match else "").lower()
            fence_body = []
            fence_lineno = lineno
            in_fence = True
    return errors


def find_bare_blob_errors(path):
    """整行仅为链接且紧贴（可夹空行）代码围栏时判失败。"""
    errors = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("```"):
            continue
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j >= 0 and BARE_LINK_LINE_RE.match(lines[j].strip()):
            errors.append(
                f"{path.relative_to(REPO_ROOT)}:{j + 1}: "
                f"整行链接贴围栏，改嵌进同节导语句"
            )
    return errors


def find_heading_length_warnings(qmd_files):
    """`##` 标题超过汉字数上限时记 WARN，返回 [(文件, 行号, 汉字数)]。"""
    warnings = []
    for path in qmd_files:
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if line.startswith("## "):
                han = len(HAN_RE.findall(line))
                if han > H2_HAN_LIMIT:
                    warnings.append((path, lineno, han))
    return warnings


def main() -> int:
    reexec_under_configured_python()
    parser = argparse.ArgumentParser(
        description="content 侧压缩黑话与语气禁词检查（默认全量 qmd）"
    )
    parser.add_argument("--paths", nargs="+", metavar="PATH",
                        help="只检查指定 qmd 文件或目录（相对仓库根）")
    parser.add_argument("--changed", action="store_true",
                        help="只检查 git 工作区改动的 qmd")
    args = parser.parse_args()
    if args.paths and args.changed:
        print("失败  --paths 与 --changed 不能同时使用")
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if sys.version_info < MIN_PYTHON:
        required = ".".join(map(str, MIN_PYTHON))
        print(f"失败  Python 需要 >= {required}，当前为 {sys.version.split()[0]}")
        return 1

    qmd_files = resolve_qmd_paths(args)
    scope = "全量" if not (args.paths or args.changed) else "按指定范围"
    print(f"{CYAN}==> 禁用词扫描{RESET}")
    print(f"扫描 {len(qmd_files)} 个 qmd 文件（{scope}）")
    findings = scan(qmd_files)
    for path, lineno, term in findings:
        print(f"{RED}  {path.relative_to(REPO_ROOT)}:{lineno}: 禁用词“{term}”{RESET}")
    context_errors = []
    for path in qmd_files:
        context_errors.extend(find_context_errors(path))
    for error in context_errors:
        print(f"{RED}  {error}{RESET}")
    heading_warnings = find_heading_length_warnings(qmd_files)
    if heading_warnings:
        print("以下 `##` 标题超过 10 个汉字（WARN，不判失败）：")
        for path, lineno, han in heading_warnings:
            print(f"  {path.relative_to(REPO_ROOT)}:{lineno}（{han} 个汉字）")
    if findings or context_errors:
        print(
            f"{RED}未通过：正文出现压缩黑话、电报省略、语气禁词、"
            f"裸 Status 简称或超宽 LR 图（详见上方）{RESET}"
        )
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
