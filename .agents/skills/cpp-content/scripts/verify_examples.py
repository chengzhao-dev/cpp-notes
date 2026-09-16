#!/usr/bin/env python3
"""编译校验仓库中的 C++ 示例，确保文档随附正确可运行的代码。

编译环境：Windows 调用 wsl.exe，按需启动默认 WSL2 Ubuntu，再使用 clang++ 和 libc++。
Linux（如 CI）直接在本地编译。脚本不会保持 WSL 常驻会话。
用法：
  python verify_examples.py
  python verify_examples.py --compiler clang++
  python verify_examples.py --style        # 追加 clang-format / clang-tidy
  python verify_examples.py --paths code/language-basics/types-and-variables.cpp content/language-basics/types-and-variables.qmd

Windows 下使用仓库配置的 Python 3.12 运行：
  python .agents/skills/agent-ops/scripts/run.py verify
退出码：0 = 全部通过，1 = 至少一处失败。

编译阶段：
  1. code/ 下书籍示例（规范见 references/cpp/engineering.md，-std=c++20 -Wall -Wextra）。
     含 CMakeLists.txt 的目录按完整 CMake 工程构建，工程内源码不再逐个独立编译
  2. 本 skill references/cpp/*.md 内嵌完整示例（含 int main 的 ```cpp 块）
  3. content/**/*.qmd 内嵌完整示例
风格阶段（仅 --style，规范见 references/cpp/code-style.md）：
  S1. clang-format --dry-run -Werror 检查 code/**.cpp（硬门槛）
  S2. clang-tidy 检查 code/**.cpp（仅输出报告，不计失败）
  配置显式指向 .agents/skills/cpp-content/assets/config/（.clang-format、.clang-tidy）。
  clang 工具缺失/过旧时降级为警告。编译始终是硬门槛。
"""

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

BLOCK_RE = re.compile(r"`{3}(?:\{\.cpp[^`]*\}|cpp)\r?\n(.*?)`{3}", re.S)
MAIN_RE = re.compile(r"int\s+main\s*\(")
SKIP_RE = re.compile(r"//\s*verify-skip")
CMAKE_RE = re.compile(r"^CMakeLists\.txt$")
CPP_EXTENSIONS = {".cc", ".cpp", ".cxx"}
# 构建产物目录：不属于书籍示例，一律不编译、不做风格检查
SKIP_DIRS = {"build", ".git", "__pycache__", ".venv"}

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
CPP_CONFIG_DIR = SKILL_ROOT / "assets" / "config"
sys.path.insert(0, str(REPO_ROOT / ".agents" / "skills" / "python-tools" / "scripts"))
from temp_paths import temp_dir  # noqa: E402


ON_WINDOWS = platform.system() == "Windows"


def tool_major_version(tool):
    """返回编译环境内工具的主版本号。无法探测时返回 0。"""
    result = sh(f"{tool} --version 2>&1")
    m = re.search(r"version\s+(\d+)\.", result.stdout or "")
    return int(m.group(1)) if m else 0


def to_env_path(native_path):
    """Windows 上把 D:\\dir\\f.cpp 转成 WSL 可见的 /mnt/d/dir/f.cpp，Linux 原样返回。"""
    native_path = os.fspath(native_path)
    if not ON_WINDOWS:
        return native_path
    drive = native_path[0].lower()
    return "/mnt/" + drive + native_path[2:].replace("\\", "/")


def tidy_diagnostics(text, repo_root):
    """只保留仓库源码中的 clang-tidy 诊断，过滤 WSL 环境和汇总噪声。"""
    marker = to_env_path(repo_root).replace("\\", "/").lower()
    diagnostics = []
    for raw in text.splitlines():
        line = " ".join(raw.replace("\x00", "").split())
        lower = line.lower()
        if not line or marker not in lower:
            continue
        if "warning:" in lower or "error:" in lower or "note:" in lower:
            diagnostics.append(line)
    return diagnostics


def sh(cmd, timeout=120):
    """在编译环境执行命令。Windows 经 WSL 按需启动 Ubuntu。"""
    argv = ["wsl", "bash", "-c", cmd] if ON_WINDOWS else ["bash", "-c", cmd]
    env = None
    if ON_WINDOWS:
        env = os.environ.copy()
        env["WSL_UTF8"] = "1"
    return subprocess.run(
        argv,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout, env=env,
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


def compile_database(path):
    """返回源文件所在 CMake 工程的构建目录。没有 compile_commands.json 时返回空。"""
    current = Path(path).resolve().parent
    while current != current.parent:
        build_dir = current / "build"
        if (build_dir / "compile_commands.json").is_file():
            return build_dir
        current = current.parent
    return None


def compile_source(compiler, standard, env_path, out_name):
    cmd = (f"{compiler} -std={standard} -stdlib=libc++ -Wall -Wextra "
           f"-o /tmp/{out_name} '{env_path}' 2>&1")
    return sh(cmd)


def compile_block(compiler, standard, body, label):
    """编译一个从 markdown 抽出的 cpp 代码块。返回 (ok, message)。"""
    directory = temp_dir("runtime")
    tmp = directory / "__qmd_block.cpp"
    with tmp.open("w", encoding="utf-8", newline="\n") as fh:
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


def path_within(path, directory):
    """判断 path 是否位于 directory 内，使用规范化绝对路径比较。"""
    try:
        return os.path.commonpath([path, directory]) == directory
    except ValueError:
        return False


def find_cmake_projects(src_dir):
    """返回每个 CMake 工程根目录，遇到工程根后不再进入其子目录。"""
    projects = []
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if any(CMAKE_RE.match(name) for name in filenames):
            projects.append(os.path.normpath(dirpath))
            dirnames[:] = []
    return sorted(projects)


def cmake_project_cpp_files(project):
    """返回工程内需要做风格检查的 C++ 源文件。"""
    files = []
    for dirpath, dirnames, filenames in os.walk(project):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        files.extend(
            os.path.normpath(os.path.join(dirpath, name))
            for name in filenames
            if Path(name).suffix.lower() in CPP_EXTENSIONS
        )
    return sorted(files)


def build_cmake_project(project, repo_root, compiler):
    """在 temp/verify-build 下重新配置并构建一个 CMake 工程。"""
    rel = os.path.relpath(project, repo_root)
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", rel).strip("-") or "project"
    build_root = temp_dir("verify-build").resolve()
    build_dir = (build_root / slug).resolve()
    if build_root not in build_dir.parents:
        raise RuntimeError(f"unexpected CMake build directory: {build_dir}")
    if build_dir.is_dir():
        shutil.rmtree(build_dir)

    cmd = (
        f"cmake -S '{to_env_path(project)}' -B '{to_env_path(build_dir)}' "
        f"-G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER='{compiler}' && "
        f"cmake --build '{to_env_path(build_dir)}'"
    )
    return sh(cmd, timeout=300)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", default="clang++")
    parser.add_argument("--standard", default="c++20")
    parser.add_argument("--source-dir", default="code")
    parser.add_argument("--paths", nargs="*", help="只校验指定的 .cpp 或 .qmd 文件")
    parser.add_argument("--style", action="store_true",
                        help="追加 clang-format（硬门槛）与 clang-tidy（报告）检查")
    args = parser.parse_args()

    repo_root = os.getcwd()
    selected_paths = {
        os.path.normpath(os.path.join(repo_root, path))
        for path in (args.paths or [])
    }
    consumed_paths = set()
    fail = 0
    style_targets = []

    if not env_available():
        print("未检测到可用的编译环境（Windows 需 WSL2，Linux 需 bash + clang++）。")
        print("Windows：wsl --install 后在 WSL2 内装 clang、libc++ 和构建工具。")
        return 1

    # ---------- 阶段 1：code/ 目录 ----------
    src_dir = os.path.join(repo_root, args.source_dir)
    cpp_files = []
    cmake_projects = []
    if os.path.isdir(src_dir):
        for dirpath, dirnames, filenames in os.walk(src_dir):
            # 原地剪枝：不进入 build/ 等目录，避免把 CMake 生成物当示例校验
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            cpp_files.extend(
                os.path.normpath(os.path.join(dirpath, fn))
                for fn in filenames
                if Path(fn).suffix.lower() in CPP_EXTENSIONS
                and (not args.paths or os.path.normpath(os.path.join(dirpath, fn)) in selected_paths)
            )
        cpp_files.sort()
        cmake_projects = find_cmake_projects(src_dir)

    selected_projects = [
        project for project in cmake_projects
        if not args.paths or any(path_within(path, project) for path in selected_paths)
    ]
    all_project_cpp = {
        project: cmake_project_cpp_files(project) for project in cmake_projects
    }

    if cpp_files or selected_projects:
        print(
            f"=== Phase 1: book examples under {args.source_dir} "
            f"({len(cpp_files)} cpp, {len(selected_projects)} CMake project(s)) ==="
        )
        for project in selected_projects:
            rel_project = os.path.relpath(project, repo_root)
            print(f"cmake build: {rel_project}")
            result = build_cmake_project(project, repo_root, args.compiler)
            if result.returncode == 0:
                print("  OK")
            else:
                fail += 1
                out = "\n".join(
                    (result.stdout or "").splitlines()
                    + (result.stderr or "").splitlines()
                )
                for line in out.splitlines():
                    print(f"    {line}")
            style_targets.extend(all_project_cpp[project])
            consumed_paths.update(
                path for path in selected_paths if path_within(path, project)
            )

        for f in cpp_files:
            if any(path_within(f, project) for project in cmake_projects):
                continue
            rel = os.path.relpath(f, repo_root)
            consumed_paths.add(f)
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
        print(f"Phase 1: no C++ examples under {args.source_dir}, skipped.")

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
            if args.paths and os.path.normpath(ref_file) not in selected_paths:
                continue
            consumed_paths.add(os.path.normpath(ref_file))
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
            if args.paths and os.path.normpath(qf) not in selected_paths:
                continue
            consumed_paths.add(os.path.normpath(qf))
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

    unmatched = sorted(selected_paths - consumed_paths)
    if unmatched:
        fail += 1
        print()
        print("=== Unconsumed selected paths ===")
        for path in unmatched:
            print(f"  FAIL {os.path.relpath(path, repo_root)}")

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
                build_dir = compile_database(f)
                if build_dir:
                    result = sh(
                        f"clang-tidy --quiet {tidy_arg} "
                        f"-p '{to_env_path(build_dir)}' '{to_env_path(f)}' 2>&1"
                    )
                else:
                    result = sh(f"clang-tidy --quiet {tidy_arg} '{to_env_path(f)}' "
                                f"-- -std=c++20 -stdlib=libc++ 2>&1")
                out = "\n".join((result.stdout or "").splitlines() + (result.stderr or "").splitlines())
                diagnostics = tidy_diagnostics(out, repo_root)
                for line in diagnostics:
                    print(f"    {line}")
                if not diagnostics and result.returncode == 0:
                    print("  clean")
                elif not diagnostics:
                    print("    tidy did not complete (informational)")

    # ---------- 汇总 ----------
    print()
    if fail == 0:
        print("All examples compiled successfully.")
        return 0
    print(f"{fail} example(s) failed; fix before rendering.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
