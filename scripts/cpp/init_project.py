#!/usr/bin/env python3
"""生成最小 C++ 项目骨架。

布局（--layout，默认 auto）：
  bare   仅 main.cpp，适合 code/<part>/ 单文件校验。
  simple main.cpp + CMakeLists.txt + .gitignore。
  auto   目标在仓库 code/ 下 -> bare，否则 -> simple。

用法：python scripts/cpp/init_project.py --name <name> [--dir code/<part>]
退出码：0 成功；1 参数/路径错误。
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
PLACEHOLDER = "{{PROJECT_NAME}}"
LAYOUTS = ("auto", "bare", "simple")

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
REPO_ROOT = SCRIPT_DIR.parent.parent


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  create {path}")


def render(template_path, target_path, name):
    text = template_path.read_text(encoding="utf-8")
    write(target_path, text.replace(PLACEHOLDER, name))


def setup_clang_configs(target_dir, no_clang):
    if no_clang:
        return
    for name in (".clang-format", ".clang-tidy"):
        bundled = TEMPLATE_DIR / name.lstrip(".")
        if bundled.is_file():
            shutil.copyfile(bundled, target_dir / name)
            print(f"  copy   {name}")


def readme_text(name, layout):
    lines = [f"# {name}", ""]
    if layout == "bare":
        lines += [
            "单文件验证：",
            "",
            "```bash",
            "python .cursor/skills/cpp-content/scripts/verify_examples.py",
            "```",
        ]
    else:
        lines += [
            "构建：",
            "",
            "```bash",
            "cmake -S . -B build",
            "cmake --build build",
            "./build/bin/app",
            "```",
        ]
    return "\n".join(lines) + "\n"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="项目名（纯 ASCII）")
    parser.add_argument("--dir", default="code", help="目标父目录")
    parser.add_argument("--layout", choices=LAYOUTS, default="auto")
    parser.add_argument("--readme", action="store_true")
    parser.add_argument("--no-clang", action="store_true")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        print(f"错误：--name 必须为纯 ASCII，收到：{args.name}")
        return 1

    target = Path(args.dir) / args.name
    if target.exists() and any(target.iterdir()):
        print(f"错误：目标目录已存在且非空：{target}")
        return 1

    layout = args.layout
    if layout == "auto":
        try:
            target.resolve().relative_to(REPO_ROOT / "code")
            layout = "bare"
        except ValueError:
            layout = "simple"
    print(f"布局：{layout}（目标：{target}）")

    name = args.name
    if layout == "bare":
        write(target / "main.cpp", (TEMPLATE_DIR / "main.cpp").read_text(encoding="utf-8"))
    else:
        render(TEMPLATE_DIR / "main.cpp", target / "main.cpp", name)
        render(TEMPLATE_DIR / "CMakeLists.txt", target / "CMakeLists.txt", name)
        write(target / ".gitignore", (TEMPLATE_DIR / "gitignore").read_text(encoding="utf-8"))

    setup_clang_configs(target, args.no_clang)
    if args.readme:
        write(target / "README.md", readme_text(name, layout))

    print("\n下一步：编辑源码并运行 verify_examples.py 或 cmake 构建。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
