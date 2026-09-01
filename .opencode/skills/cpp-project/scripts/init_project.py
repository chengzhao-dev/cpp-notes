#!/usr/bin/env python3
"""生成最小 C++ 项目骨架（只生成内容，不涉及任何 IDE）。

三档布局（--layout，默认 auto）：
  bare    仅 main.cpp —— 适合 code/<主题>/ 下的单文件验证代码，
          由 cpp-content 的 verify_examples.py 直接编译。
  simple  main.cpp + CMakeLists.txt + .gitignore —— 可独立构建的最小组件。
  full    src/ + include/<name>/ + tests/ + CMakePresets.json
          （debug / release / sanitize）—— 组合用法（库 + 测试 + 预设）。
  auto    目标目录在本仓库 code/ 下 -> bare；否则 -> simple。

clang 配置（.clang-format / .clang-tidy）：
  统一从本 skill 内置模板复制到新工程（仓库根不放配置文件）；
  --no-clang 可显式关闭复制。

用法：
  python init_project.py --name <name> [--dir <parent>]
                         [--layout auto|bare|simple|full] [--readme] [--no-clang]
退出码：0 = 生成成功；1 = 参数/路径错误。
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
PLACEHOLDER = "{{PROJECT_NAME}}"
LAYOUTS = ("auto", "bare", "simple", "full")

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_ROOT / "templates"
REPO_ROOT = Path(__file__).resolve().parents[4]


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
    copied = False
    for name in (".clang-format", ".clang-tidy"):
        bundled = TEMPLATE_DIR / name.lstrip(".")
        if bundled.is_file():
            shutil.copyfile(bundled, target_dir / name)
            print(f"  copy   {name}  (bundled template)")
            copied = True
    if not copied:
        print("  警告：未找到内置 clang 配置模板，已跳过。")


def readme_text(name, layout):
    lines = [f"# {name}", ""]
    if layout == "bare":
        lines += [
            "单文件验证代码，由本仓库的 verify_examples.py 直接编译：",
            "",
            "```bash",
            "python .opencode/skills/cpp-content/scripts/verify_examples.py",
            "```",
        ]
    elif layout == "simple":
        lines += [
            "最小可构建组件：",
            "",
            "```bash",
            "cmake -S . -B build",
            "cmake --build build",
            "./build/" + name,
            "```",
        ]
    else:
        lines += [
            "库 + 测试 + 预设（debug / release / sanitize）：",
            "",
            "```bash",
            "cmake --preset debug",
            "cmake --build build/debug",
            "ctest --test-dir build/debug",
            "./build/debug/" + name,
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
    parser.add_argument("--name", required=True, help="项目/目录名（纯 ASCII：字母/数字/-/_，建议小写）")
    parser.add_argument("--dir", default="code", help="目标父目录（默认 code/）")
    parser.add_argument("--layout", choices=LAYOUTS, default="auto", help="骨架布局（默认 auto）")
    parser.add_argument("--readme", action="store_true", help="同时生成 README.md（默认不生成）")
    parser.add_argument("--no-clang", action="store_true", help="不复制 .clang-format / .clang-tidy")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        print(f"错误：--name 必须为纯 ASCII（字母/数字/-/_），收到：{args.name}")
        return 1

    parent = Path(args.dir)
    target = parent / args.name
    if target.exists() and any(target.iterdir()):
        print(f"错误：目标目录已存在且非空（中止）：{target}")
        return 1

    # auto 布局：仓库 code/ 下 -> bare，否则 -> simple
    layout = args.layout
    if layout == "auto":
        try:
            under_code = target.resolve().relative_to(REPO_ROOT / "code")
            layout = "bare"
        except ValueError:
            layout = "simple"
    print(f"布局：{layout}（目标：{target}）")

    name = args.name
    if layout == "bare":
        write(target / "main.cpp", (TEMPLATE_DIR / "main.cpp").read_text(encoding="utf-8"))
    elif layout == "simple":
        render(TEMPLATE_DIR / "main.cpp", target / "main.cpp", name)
        render(TEMPLATE_DIR / "CMakeLists.txt", target / "CMakeLists.txt", name)
        write(target / ".gitignore", (TEMPLATE_DIR / "gitignore").read_text(encoding="utf-8"))
    else:  # full
        render(TEMPLATE_DIR / "full" / "CMakeLists.txt", target / "CMakeLists.txt", name)
        render(TEMPLATE_DIR / "full" / "CMakePresets.json", target / "CMakePresets.json", name)
        write(target / ".gitignore", (TEMPLATE_DIR / "gitignore").read_text(encoding="utf-8"))
        render(TEMPLATE_DIR / "full" / "main.cpp", target / "src" / "main.cpp", name)
        render(TEMPLATE_DIR / "full" / "lib.cpp.tpl", target / "src" / f"{name}.cpp", name)
        render(TEMPLATE_DIR / "full" / "lib.h.tpl", target / "include" / name / f"{name}.h", name)
        render(TEMPLATE_DIR / "full" / "tests_CMakeLists.txt", target / "tests" / "CMakeLists.txt", name)
        render(TEMPLATE_DIR / "full" / "test_main.cpp", target / "tests" / "test_main.cpp", name)

    setup_clang_configs(target, args.no_clang)
    if args.readme:
        write(target / "README.md", readme_text(name, layout))

    print()
    print("下一步：")
    if layout == "bare":
        print(f"  1. 编辑 {target / 'main.cpp'}")
        print("  2. 运行 python .opencode/skills/cpp-content/scripts/verify_examples.py 编译校验")
    elif layout == "simple":
        print(f"  1. cd {target}")
        print("  2. cmake -S . -B build && cmake --build build")
    else:
        print(f"  1. cd {target}")
        print("  2. cmake --preset debug && cmake --build build/debug")
        print("  3. ctest --test-dir build/debug")
    return 0


if __name__ == "__main__":
    sys.exit(main())
