#!/usr/bin/env python3
"""编译校验仓库中的 C++ 示例，确保文档随附正确可运行的代码。

编译环境：Windows 调用 wsl.exe，按需启动默认 WSL2 Ubuntu，再使用 g++/clang++；
Linux（如 CI）直接在本地编译。脚本不会保持 WSL 常驻会话。
用法：
  python verify_examples.py
  python verify_examples.py --compiler clang++
  python verify_examples.py --style        # 追加 clang-format / clang-tidy

Windows 下建议从仓库配置的 Python 3.12 运行：
  D:/ProgramData/miniforge3/python.exe D:/Github/cpp-notes/scripts/agent/run.py verify
退出码：0 = 全部通过；1 = 至少一处失败。

编译阶段：
  1. code/ 下书籍示例（规范见 references/cpp/toolchain.md，-std=c++20 -Wall -Wextra）；
     跳过 build/ 等构建目录，不校验 CMake 生成物
  2. 本 skill references/cpp/*.md 内嵌完整示例（含 int main 的 ```cpp 块）
  3. content/**/*.qmd 内嵌完整示例
风格阶段（仅 --style；规范见 references/cpp/code-style.md）：
  S1. clang-format --dry-run -Werror 检查 code/**.cpp（硬门槛）
  S2. clang-tidy 检查 code/**.cpp（仅输出报告，不计失败）
  配置显式指向 .config/cpp/（.clang-format、.clang-tidy）；
  clang 工具缺失/过旧时降级为警告；编译始终是硬门槛。
"""

import argparse
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BLOCK_RE = re.compile(r"`{3}(?:\{\.cpp[^`]*\}|cpp)\r?\n(.*?)`{3}", re.S)
MAIN_RE = re.compile(r"int\s+main\s*\(")
SKIP_RE = re.compile(r"//\s*verify-skip")
# 构建产物目录：不属于书籍示例，一律不编译、不做风格检查
SKIP_DIRS = {"build", ".git", "__pycache__", ".venv"}

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
CPP_CONFIG_DIR = REPO_ROOT / ".config" / "cpp"


ON_WINDOWS = platform.system() == "Windows"


def tool_major_version(tool):
    """返回编译环境内工具的主版本号；无法探测时返回 0。"""
    result = sh(f"{tool} --version 2>&1")
    m = re.search(r"version\s+(\d+)\.", result.stdout or "")
    return int(m.group(1)) if m else 0


def to_env_path(native_path):
    """Windows 上把 D:\\dir\\f.cpp 转成 WSL 可见的 /mnt/d/dir/f.cpp；Linux 原样返回。"""
    if not ON_WINDOWS:
        return native_path
    drive = native_path[0].lower()
    return "/mnt/" + drive + native_path[2:].replace("\\", "/")


def sh(cmd, timeout=120):
    """在编译环境执行命令；Windows 经 WSL 按需启动 Ubuntu。"""
    argv = ["wsl", "bash", "-c", cmd] if ON_WINDOWS else ["bash", "-c", cmd]
    return subprocess.run(
        argv,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )


def env_available():
    """编译环境是否可用：Windows 探测 WSL，Linux 探测 bash。"""
    try:
        return sh("true", timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def env_tool_exists(tool):
    try:
        return sh(f"command -v '{tool}' > /dev/null 2>&1").returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def compile_source(compiler, standard, env_path, out_name):
    cmd = f"{compiler} -std={standard} -Wall -Wextra -o /tmp/{out_name} '{env_path}' 2>&1"
    return sh(cmd)


def compile_block(compiler, standard, body, label):
    """编译一个从 markdown 抽出的 cpp 代码块；返回 (ok, message)。"""
    fd, tmp = tempfile.mkstemp(suffix=".cpp", prefix="__qmd_block_")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    try:
        result = compile_source(compiler, standard, to_env_path(tmp), "__qmd_block")
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

    if not env_available():
        print("未检测到可用的编译环境（Windows 需 WSL2，Linux 需 bash + g++/clang++）。")
        print("Windows：wsl --install 后在 WSL2 内装 build-essential。")
        return 1

    # ---------- 阶段 1：code/ 目录 ----------
    src_dir = os.path.join(repo_root, args.source_dir)
    cpp_files = []
    if os.path.isdir(src_dir):
        for dirpath, dirnames, filenames in os.walk(src_dir):
            # 原地剪枝：不进入 build/ 等目录，避免把 CMake 生成物当示例校验
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            cpp_files.extend(
                os.path.join(dirpath, fn)
                for fn in filenames if fn.endswith(".cpp")
            )
        cpp_files.sort()
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
            result = compile_source(args.compiler, args.standard, to_env_path(f), "__qmd_check")
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
    ref_dir = str(SKILL_ROOT / "references" / "cpp")
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
        if not env_tool_exists("clang-format") or not env_tool_exists("clang-tidy"):
            print("编译环境内未找到 clang-format/clang-tidy，风格检查跳过（非致命）。")
            print("安装：sudo apt install clang-format clang-tidy")
        elif not style_targets:
            print("  no compilable .cpp under code/, nothing to check.")
        else:
            fmt_cfg = to_env_path(str(CPP_CONFIG_DIR / ".clang-format"))
            tidy_cfg = to_env_path(str(CPP_CONFIG_DIR / ".clang-tidy"))
            fmt_arg = (f"--style=file:'{fmt_cfg}'"
                       if tool_major_version("clang-format") >= 14 else "")
            tidy_arg = (f"--config-file='{tidy_cfg}'"
                        if tool_major_version("clang-tidy") >= 12 else "")
            if not fmt_arg or not tidy_arg:
                print("  clang-format/clang-tidy 版本过旧，无法显式指定 skill 模板配置，"
                      "回退到工程内 .clang-format/.clang-tidy 向上发现。")
            for f in style_targets:
                rel = os.path.relpath(f, repo_root)
                print(f"format: {rel}")
                result = sh(f"clang-format {fmt_arg} --dry-run -Werror '{to_env_path(f)}' 2>&1")
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
                result = sh(f"clang-tidy --quiet {tidy_arg} '{to_env_path(f)}' -- -std=c++20 2>&1")
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
