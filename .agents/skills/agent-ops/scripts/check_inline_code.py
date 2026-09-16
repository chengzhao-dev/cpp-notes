#!/usr/bin/env python3
"""检查正文中的关键技术标识是否使用统一的行内代码标记。"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[4]
TOOLS = ("clang++", "clangd", "lldb", "CMake")
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_+.-])(%s)(?![A-Za-z0-9_+.-])" % "|".join(map(re.escape, TOOLS)))


def prose_lines(text: str):
    in_fence = False
    in_frontmatter = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line_no == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
            continue
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            if line.lstrip().startswith("#"):
                continue
            yield line_no, line


def unmarked(line: str):
    # Remove complete code spans and link destinations before checking prose.
    clean = re.sub(r"`[^`]*`", "", line)
    clean = re.sub(r"\[[^\]]*\]\([^)]*\)", "", clean)
    return TOKEN_RE.findall(clean)


def main() -> int:
    findings = []
    for path in sorted((ROOT / "content").rglob("*.qmd")):
        for line_no, line in prose_lines(path.read_text(encoding="utf-8")):
            for token in unmarked(line):
                findings.append(f"{path.relative_to(ROOT).as_posix()}:{line_no}: {token} 应使用反引号")
    if findings:
        print(f"FAIL inline-code 未标记={len(findings)}")
        for item in findings[:40]:
            print(f"      {item}")
        return 1
    print("PASS inline-code 关键工具标记一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
