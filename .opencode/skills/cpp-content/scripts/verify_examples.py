#!/usr/bin/env python3
"""编译校验仓库中的 C++ 示例，确保文档随附正确可运行的代码。

默认环境：Windows 上的 WSL2（g++/clang++）。
用法：
  python verify_examples.py
  python verify_examples.py --compiler clang++
  python verify_examples.py --style        # 追加 clang-format / clang-tidy
退出码：0 = 全部通过；1 = 至少一处失败。

编译阶段：
  1. code/ 下书籍示例（规范见 references/cpp/toolchain.md，-std=c++20 -Wall -Wextra）
  2. 本 skill references/cpp/*.md 内嵌完整示例（含 int main 的 ```cpp 块）
  3. content/**/*.qmd 内嵌完整示例
风格阶段（仅 --style；规范见 references/cpp/code-style.md）：
  S1. clang-format --dry-run -Werror 检查 code/**.cpp（硬门槛）
  S2. clang-tidy 检查 code/**.cpp（仅输出报告，不计失败）
clang 工具缺失时降级为警告；编译始终是硬门槛。
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

BLOCK_RE = re.compile(r"`{3}(?:\{\.cpp[^`]*\}|cpp)\r?\n(.*?)`{3}", re.S)
MAIN_RE = re.compile(r"int\s+main\s*\(")
SKIP_RE = re.compile(r"//\s*verify-skip")


def to_wsl_path(win_path):
    """D:\\dir\\file.cpp -> /mnt/d/dir/file.cpp"""
    drive = win_path[0].lower()
    return "/mnt/" + drive + win_path[2:].replace("\\", "/")


def wsl(cmd, timeout=120):
    return subprocess.run(
        ["wsl", "bash", "-c", cmd],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )


def wsl_available():
    try:
        return wsl("true", timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def wsl_tool_exists(tool):
    try:
        return wsl(f"command -v '{tool}' > /dev/null 2>&1").returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def compile_source(compiler, standard, wsl_path, out_name):
    cmd = f"{compiler} -std={standard} -Wall -Wextra -o /tmp/{out_name} '{wsl_path}' 2>&1"
    return wsl(cmd)


def compile_block(compiler, standard, body, label):
    """编译一个从 markdown 抽出的 cpp 代码块；返回 (ok, message)。"""
    fd, tmp = tempfile.mkstemp(suffix=".cpp", prefix="__qmd_block_")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    try:
        result = compile_source(compiler, standard, to_wsl_path(tmp), "__qmd_block")
        if result.returncode == 0:
            return True, f"  OK   {label}"
        msg = "\n".join((result.stdout or "").splitlines() + (result.stderr or "").splitlines())
        return False, f"  FAIL {label}\n{msg}"
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def extract_full_blocks(path):
    """返回文件中含 int main 的 ```cpp 块列表 [(序号, 内容)]。"""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    blocks = []
    for i, m in enumerate(BLOCK_RE.finditer(text), start=1):
        body = m.group(1)
        if MAIN_RE.search(body):
            blocks.append((i, body))
    return blocks


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", default="g++")
    parser.add_argument("--standard", default="c++20")
    parser.add_argument("--source-dir", default="code")
    parser.add_argument("--style", action="store_true",
                        help="追加 clang-format（硬门槛）与 clang-tidy（报告）检查")
    args = parser.parse_args()

    repo_root = os.getcwd()
    fail = 0
    style_targets = []

    if not wsl_available():
        print("WSL2 未检测到，无法在默认环境编译。")
        print("请在 WSL2 内运行 g++/clang++，或先安装 WSL。")
        return 1

    # ---------- 阶段 1：code/ 目录 ----------
    src_dir = os.path.join(repo_root, args.source_dir)
    cpp_files = []
    if os.path.isdir(src_dir):
        cpp_files = sorted(
            os.path.join(dirpath, fn)
            for dirpath, _, filenames in os.walk(src_dir)
            for fn in filenames if fn.endswith(".cpp")
        )
    if cpp_files:
        print(f"=== Phase 1: book examples under {args.source_dir} ({len(cpp_files)}) ===")
        for f in cpp_files:
            rel = os.path.relpath(f, repo_root)
            with open(f, encoding="utf-8", errors="replace") as fh:
                src = fh.read()
            if SKIP_RE.search(src):
                print(f"skip (verify-skip): {rel}")
                continue
            if not MAIN_RE.search(src):
                print(f"skip (no main): {rel}")
                continue
            style_targets.append(f)
            print(f"compile: {rel}")
            result = compile_source(args.compiler, args.standard, to_wsl_path(f), "__qmd_check")
            if result.returncode == 0:
                print("  OK")
            else:
                fail += 1
                out = "\n".join((result.stdout or "").splitlines() + (result.stderr or "").splitlines())
                for line in out.splitlines():
                    print(f"    {line}")
    else:
        print(f"Phase 1: no .cpp under {args.source_dir}, skipped.")

    # ---------- 阶段 2：skill references/cpp/*.md 内嵌完整示例 ----------
    ref_dir = os.path.join(repo_root, ".opencode", "skills", "cpp-content", "references", "cpp")
    print()
    print("=== Phase 2: full examples embedded in skill C++ references ===")
    total2 = 0
    if os.path.isdir(ref_dir):
        for name in sorted(os.listdir(ref_dir)):
            if not name.endswith(".md"):
                continue
            ref_file = os.path.join(ref_dir, name)
            for idx, body in extract_full_blocks(ref_file):
                total2 += 1
                ok, msg = compile_block(args.compiler, args.standard, body, f"{name[:-3]} #{idx}")
                print(msg)
                if not ok:
                    fail += 1
    if total2 == 0:
        print("  (none found)")

    # ---------- 阶段 3：content/**.qmd 内嵌完整示例 ----------
    content_dir = os.path.join(repo_root, "content")
    print()
    print("=== Phase 3: inline cpp examples in content/**.qmd ===")
    total3 = 0
    if os.path.isdir(content_dir):
        qmd_files = sorted(
            os.path.join(dirpath, fn)
            for dirpath, _, filenames in os.walk(content_dir)
            for fn in filenames if fn.endswith(".qmd")
        )
        for qf in qmd_files:
            rel = os.path.relpath(qf, repo_root)
            for idx, body in extract_full_blocks(qf):
                total3 += 1
                ok, msg = compile_block(args.compiler, args.standard, body, f"{rel} #{idx}")
                print(msg)
                if not ok:
                    fail += 1
        if total3 == 0:
            print("  (none found)")
    else:
        print("  content/ not found, skipped.")

    # ---------- 风格阶段：clang-format（硬门槛）+ clang-tidy（报告） ----------
    if args.style:
        print()
        print("=== Style check: clang-format + clang-tidy (per references/cpp/code-style.md) ===")
        if not wsl_tool_exists("clang-format") or not wsl_tool_exists("clang-tidy"):
            print("WSL 内未找到 clang-format/clang-tidy，风格检查跳过（非致命）。")
            print("安装：sudo apt install clang-format clang-tidy")
        elif not style_targets:
            print("  no compilable .cpp under code/, nothing to check.")
        else:
            for f in style_targets:
                rel = os.path.relpath(f, repo_root)
                print(f"format: {rel}")
                result = wsl(f"clang-format --dry-run -Werror '{to_wsl_path(f)}' 2>&1")
                if result.returncode == 0:
                    print("  OK")
                else:
                    fail += 1
                    out = "\n".join((result.stdout or "").splitlines() + (result.stderr or "").splitlines())
                    for line in out.splitlines():
                        print(f"    {line}")
            for f in style_targets:
                rel = os.path.relpath(f, repo_root)
                print(f"tidy: {rel} (informational)")
                result = wsl(f"clang-tidy --quiet '{to_wsl_path(f)}' -- -std=c++20 2>&1")
                out = "\n".join((result.stdout or "").splitlines() + (result.stderr or "").splitlines())
                for line in out.splitlines():
                    print(f"    {line}")
                if not out.strip():
                    print("  clean")

    # ---------- 汇总 ----------
    print()
    if fail == 0:
        print("All examples compiled successfully.")
        return 0
    print(f"{fail} example(s) failed; fix before rendering.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
