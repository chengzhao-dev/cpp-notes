#!/usr/bin/env python3
"""按文档类型检查仓库 Markdown 与 QMD 的基础结构。"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "_book", ".quarto", "build", "node_modules"}
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
IMAGE = re.compile(r"!\[([^]]*)\]\(([^)]+)\)")
CALLOUT = re.compile(r"^\s*:::\s*\{\.callout-([\w-]+)\}")
CALLOUTS = {"note", "tip", "warning", "important", "caution"}
CODE_EXTENSIONS = {".cpp", ".cc", ".cxx", ".h", ".hpp", ".cmake", ".sh", ".bash"}
CODE_NAMES = {"CMakeLists.txt"}
CODE_LANGUAGES = {"cpp", "c", "bash", "sh", "shell", "powershell", "ps1", "cmake", "text", "markdown", "yaml", "json", "toml", "mermaid"}


def documents():
    paths = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "index.qmd"]
    for folder in ("content", "docs", ".cursor/skills"):
        base = ROOT / folder
        if base.is_dir():
            paths.extend(base.rglob("*.qmd" if folder == "content" else "*.md"))
    return sorted(p for p in set(paths) if p.is_file() and not any(x in p.parts for x in SKIP))


def doc_kind(path):
    if path.name == "README.md":
        return "readme"
    if path.name == "AGENTS.md":
        return "agents"
    if path.suffix == ".qmd":
        return "qmd"
    return "md"


def local_path(path, value):
    value = value.split("#", 1)[0].split("?", 1)[0].strip("<>")
    if not value or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return None
    candidate = (path.parent / value).resolve()
    if candidate.exists():
        return candidate
    if Path(value).name == "AGENTS.md":
        return (ROOT / "AGENTS.md").resolve()
    return candidate


def check(path):
    rel = path.relative_to(ROOT).as_posix()
    errors, notices = [], []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{rel}: DOC-E1 非 UTF-8"], []
    kind = doc_kind(path)
    in_fence = False
    fence_char = ""
    fence_size = 0
    fence_start = 0
    fence_info = ""
    headings = []
    blocks = []
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        match = FENCE.match(line)
        if match:
            marker, info = match.groups()
            if not in_fence:
                in_fence, fence_char, fence_size = True, marker[0], len(marker)
                fence_start, fence_info = number, info.strip()
            elif marker[0] == fence_char and len(marker) >= fence_size:
                blocks.append((fence_start, number, fence_info))
                in_fence = False
            continue
        if not in_fence:
            heading = HEADING.match(line)
            if heading:
                headings.append((number, len(heading.group(1)), heading.group(2)))
                if kind in {"qmd", "readme", "agents"} and "`" in heading.group(2):
                    errors.append(f"{rel}:{number}: DOC-E2 标题不应使用反引号")
                elif "`" in heading.group(2):
                    notices.append(f"{rel}:{number}: DOC-N4 标题含反引号，请确认是否便于检索")
            callout = CALLOUT.match(line)
            if callout and callout.group(1) not in CALLOUTS:
                errors.append(f"{rel}:{number}: DOC-E3 callout 类型不受支持")
    if in_fence:
        errors.append(f"{rel}:{fence_start}: DOC-E4 代码围栏未闭合")
    previous = 0
    for number, level, _title in headings:
        if previous and level > previous + 1:
            errors.append(f"{rel}:{number}: DOC-E5 标题层级跳跃")
        previous = level
    for start, end, info in blocks:
        language = info.split()[0] if info else ""
        if language == "{mermaid}":
            language = "mermaid"
        body = "\n".join(lines[start:end - 1])
        if kind == "qmd":
            if language == "mermaid" and not info.startswith("{mermaid}"):
                errors.append(f"{rel}:{start}: DOC-E6 Mermaid 必须使用 {{mermaid}} 围栏")
            if language and language not in CODE_LANGUAGES:
                notices.append(f"{rel}:{start}: DOC-N5 未登记的代码块语言 {language}，请确认高亮器支持")
            if language in {"bash", "powershell", "sh", "shell"} and ("$ " in body or "PS>" in body):
                errors.append(f"{rel}:{start}: DOC-E7 带提示符的命令输出应改用 text 代码块")
            if re.search(r"\*\*|(?<!\*)\*(?!\*)", body):
                notices.append(f"{rel}:{start}: DOC-N1 代码块含强调符号，请人工确认")
            if language in {"bash", "powershell", "sh", "shell"}:
                commands = [line.strip() for line in body.splitlines() if line.strip() and not line.lstrip().startswith("#")]
                if len(commands) <= 2 and all(command in {"wsl", "wsl ~"} for command in commands):
                    notices.append(f"{rel}:{start}: DOC-N9 短命令可直接融入正文，无需单独代码块")
        elif kind in {"md", "agents"} and language == "mermaid":
            notices.append(f"{rel}:{start}: DOC-N2 说明文档默认不使用 Mermaid")
    if kind in {"md", "agents"}:
        for number, line in enumerate(lines, 1):
            if re.match(r"^\s*(?:!\[|<img\b)", line):
                notices.append(f"{rel}:{number}: DOC-N3 说明文档图片需确认信息价值")
    for match in IMAGE.finditer(text):
        if not match.group(1).strip():
            errors.append(f"{rel}: DOC-E8 图片缺少替代文字")
        target = local_path(path, match.group(2))
        if target and not target.is_file() and kind != "readme":
            errors.append(f"{rel}: DOC-E9 图片不存在：{match.group(2)}")
    for match in LINK.finditer(text):
        target = local_path(path, match.group(1))
        if target and not target.exists():
            errors.append(f"{rel}: DOC-E10 本地链接不存在：{match.group(1)}")
    colon_count = sum(line.count("：") for line in lines if line.strip() and not line.lstrip().startswith(("#", "-", "```")))
    if colon_count >= 8:
        notices.append(f"{rel}: DOC-N6 正文冒号较密，请确认是否可改为完整句子")
    return errors, notices


def check_source(path):
    """检查会被 include 的源文件，重点发现行尾注释和过长解释。"""
    rel = path.relative_to(ROOT).as_posix()
    errors, notices = [], []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return [f"{rel}: DOC-E1 非 UTF-8"], []
    for number, line in enumerate(lines, 1):
        if re.search(r"\S\s+#\s+[^#]", line) and path.suffix.lower() in {".sh", ".bash"}:
            notices.append(f"{rel}:{number}: DOC-N7 行尾 Shell 注释请移到被说明代码的上一行")
        if re.search(r"\S\s+//\s+", line) and path.suffix.lower() in {".cpp", ".cc", ".cxx", ".h", ".hpp"}:
            notices.append(f"{rel}:{number}: DOC-N7 行尾 C++ 注释请移到被说明代码的上一行")
        if len(line) > 110 and line.lstrip().startswith(("#", "//")):
            notices.append(f"{rel}:{number}: DOC-N8 注释过长，请移到正文或拆成短句")
        if re.match(r"^\s*(?:wsl(?:\s+~)?|wsl\s+--(?:shutdown|terminate)\b)", line) and number > 1:
            previous = lines[number - 2].strip()
            if previous and not previous.startswith("#"):
                notices.append(f"{rel}:{number}: DOC-N9 关键命令前可补一条简短注释，说明本节学习重点")
    return errors, notices


def main():
    errors, notices = [], []
    paths = documents()
    for path in paths:
        found_errors, found_notices = check(path)
        errors.extend(found_errors)
        notices.extend(found_notices)
    source_paths = sorted(
        p for base in (ROOT / "code", ROOT / "scripts" / "cpp" / "templates")
        if base.is_dir() for p in base.rglob("*")
        if p.is_file() and (p.suffix.lower() in CODE_EXTENSIONS or p.name in CODE_NAMES)
        and not any(part in SKIP for part in p.parts)
    )
    for path in source_paths:
        found_errors, found_notices = check_source(path)
        errors.extend(found_errors)
        notices.extend(found_notices)
    for notice in notices:
        print("NOTICE " + notice)
    if errors:
        print("FAIL docs")
        for error in errors:
            print("  " + error)
        return 1
    print(f"PASS docs 分层检查（{len(paths)} 个文档）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
