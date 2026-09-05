#!/usr/bin/env python3
"""生成 C++ 项目骨架。

布局（--layout，默认 auto）：
  bare   仅 main.cpp，适合 code/<part>/ 单文件校验。
  simple main.cpp + CMakeLists.txt。
  complete 完整工程文件，适合需要直接构建的章节示例。
  auto   目标在仓库 code/ 下 -> complete，否则 -> simple。

Windows 示例（使用仓库配置的 Python 3.12）：
  D:/ProgramData/miniforge3/python.exe D:/Github/cpp-notes/scripts/cpp/init_project.py `
    --name first-program `
    --dir D:/Github/cpp-notes/code/getting-started
上例会自动创建 D:/Github/cpp-notes/code/getting-started/first-program。
随后在 WSL2 Ubuntu 中运行：
  bash /mnt/d/Github/cpp-notes/code/getting-started/first-program/build-and-run.sh

仓库根目录已配置好 Python 时，也可以使用：
  python scripts/cpp/init_project.py --name first-program --dir code/getting-started

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
LAYOUTS = ("auto", "bare", "simple", "complete")

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
REPO_ROOT = SCRIPT_DIR.parent.parent
CPP_CONFIG_DIR = REPO_ROOT / ".config" / "cpp"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  create {path}")


def render(template_path, target_path, name):
    text = template_path.read_text(encoding="utf-8")
    write(target_path, text.replace(PLACEHOLDER, name))


def setup_development_configs(target_dir, no_clang):
    if no_clang:
        return
    for name in (".clang-format", ".clang-tidy", ".clangd"):
        bundled = CPP_CONFIG_DIR / name
        if bundled.is_file():
            shutil.copyfile(bundled, target_dir / name)
            print(f"  copy   {name}")

    vscode_template = CPP_CONFIG_DIR / ".vscode"
    vscode_target = target_dir / ".vscode"
    vscode_target.mkdir(parents=True, exist_ok=True)
    for name in ("settings.json", "extensions.json"):
        bundled = vscode_template / name
        if bundled.is_file():
            shutil.copyfile(bundled, vscode_target / name)
            print(f"  copy   .vscode/{name}")


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
            "这是一个使用 CMake 管理的 C++20 项目。",
            "",
            "构建与运行：",
            "",
            "```bash",
            "cmake -S . -B build",
            "cmake --build build",
            "cd build/bin",
            "./app",
            "```",
            "",
            "配置阶段会生成 `build/compile_commands.json`，供 clangd 提供与实际构建一致的补全、跳转和诊断。",
        ]
    return "\n".join(lines) + "\n"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="项目名（纯 ASCII；它会成为最终目录名）")
    parser.add_argument("--dir", default="code", help="目标父目录；脚本会创建 --dir/--name")
    parser.add_argument(
        "--layout",
        choices=LAYOUTS,
        default="auto",
        help="项目布局：code/ 下默认 complete，其余路径默认 simple；Windows 请使用配置的 Python 3.12",
    )
    parser.add_argument("--readme", action="store_true")
    parser.add_argument(
        "--no-clang", action="store_true", help="不生成 clangd/clang-format/VSCode 配置"
    )
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        print(f"错误：--name 必须为纯 ASCII，收到：{args.name}")
        return 1

    target = Path(args.dir) / args.name
    # 目标不存在时由 write() 创建；空目录可以安全复用，非空目录拒绝覆盖。
    if target.exists() and any(target.iterdir()):
        print(f"错误：目标目录已存在且非空：{target}")
        return 1

    layout = args.layout
    if layout == "auto":
        try:
            target.resolve().relative_to(REPO_ROOT / "code")
            layout = "complete"
        except ValueError:
            layout = "simple"
    print(f"布局：{layout}（目标：{target}）")

    name = args.name
    if layout == "bare":
        write(target / "main.cpp", (TEMPLATE_DIR / "main.cpp").read_text(encoding="utf-8"))
    else:
        render(TEMPLATE_DIR / "main.cpp", target / "main.cpp", name)
        render(TEMPLATE_DIR / "CMakeLists.txt", target / "CMakeLists.txt", name)
        if layout == "complete":
            render(TEMPLATE_DIR / "build-and-run.sh", target / "build-and-run.sh", name)

    setup_development_configs(target, args.no_clang)
    if args.readme:
        write(target / "README.md", readme_text(name, layout))

    if layout == "bare":
        print("\n下一步：编辑源码并运行 verify_examples.py。")
    elif layout == "complete":
        print("\n下一步：编辑源码并运行 bash build-and-run.sh。")
    else:
        print("\n下一步：编辑源码并运行 cmake -S . -B build。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
