#!/usr/bin/env python3
"""agent 命令统一入口：把易踩坑的 Windows/PowerShell 调用包成稳定的单轮输出。

为什么需要它：省 token 的最大杠杆不是「少读文件」，而是「少几轮」。在 Windows 上
手写 PowerShell/cmd 命令常因引号与 GBK 编码失败，每次重试都把整段上下文与输出重付一遍。
渲染与校验的原始输出动辄上千行，全量回灌同样昂贵。本脚本用 Python 直接 subprocess
调用（不经 PowerShell 解析），并对输出做截断与分级：成功只回一行，失败才展开。

子命令：
  check   按 fast|book|knowledge|python|full profile 运行校验（默认 full；缺少 _book 时显示跳过）
  verify  编译校验 C++ 示例（Windows 自动经 WSL2，可 --changed 增量校验）
  render  渲染 Book 并自动跑产物校验（合并为 1 轮）
  scope   解析任务作用域，输出范围、单元、读取和禁止清单
  build   在 WSL 中跑某章节示例的一键构建（按需启动默认 Ubuntu，供 clangd 生成编译数据库）
  status  精简 git 状态：默认折叠用户既有改动，只看本次相关
  kb-index  增量或全量重建知识库索引（knowledge/ -> temp/knowledge-index/）
  kb-search  知识库单次检索（透传 retriever 参数，如 --toc/--parent/--explain）
  kb-check  知识库健康度与检索延迟测量
  kb-eval   标注集召回率与 Token 预算验收（延迟由 kb-check 负责）
  kb-scale  三层索引的规模基准（P95 拐点，验证 100MB–1GB 目标）
通用参数：
  --verbose  展开全部原始输出（仅失败排查时使用）
  --strict   仅 check：把正文分号、链接间距等软规则升级为失败
退出码：透传被包装命令的退出码，0 = 成功。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MIN_PYTHON = (3, 12)
MANIFEST = ROOT / ".agents" / "manifest.json"
TOOL_CONFIG = ROOT / ".agents" / "skills" / "python-tools" / "assets" / "config" / "runtime.json"


class ToolNotFound(RuntimeError):
    """外部工具未找到。"""


def runtime_config():
    """读取外部工具配置；不得用于选择 Python。"""
    try:
        return json.loads(TOOL_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def python_version(candidate):
    """返回解释器版本元组。无法执行时返回空值。"""
    try:
        result = subprocess.run(
            [candidate, "-c", "import sys; print(sys.version_info[:2])"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=False,
        )
        value = result.stdout.strip().strip("()")
        major, minor = (int(part.strip()) for part in value.split(","))
        return major, minor
    except (OSError, ValueError):
        return None


def select_python():
    """只使用 manifest 指定且满足最低版本的 Python。"""
    try:
        config = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    candidates = [config.get("mcp", {}).get("command")]
    seen = set()
    for candidate in candidates:
        if not candidate:
            continue
        candidate = str(candidate)
        if candidate in seen or not Path(candidate).is_file():
            continue
        seen.add(candidate)
        version = python_version(candidate)
        if version and version >= MIN_PYTHON:
            return candidate
    return None


PY = select_python()


def resolve_tool(name):
    """按环境变量、运行时配置和 PATH 顺序解析外部工具。"""
    env_name = "CPP_MEMO_" + Path(name).stem.upper()
    config = runtime_config()
    candidates = [os.environ.get(env_name), config.get(Path(name).stem), shutil.which(name)]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            # Windows 的 PATH 常先返回 .cmd 包装器。Quarto 的 .cmd 会把
            # Deno/Sass 相对路径解析到当前工作目录，优先同目录 .exe 可避免该问题。
            if Path(candidate).suffix.lower() == ".cmd":
                executable = Path(candidate).with_suffix(".exe")
                if executable.is_file():
                    return str(executable)
            return str(candidate)
    raise ToolNotFound(f"找不到工具 {name}；请配置 {env_name} 或安装后加入 PATH")

# 校验项：(名称, 脚本相对路径, 需要 _book 产物, 固定参数)
CHECKS = [
    ("empty", ".agents/skills/agent-ops/scripts/check_empty.py", False, ()),
    ("encoding", ".agents/skills/agent-ops/scripts/check_encoding.py", False, ()),
    ("agent-controls", ".agents/skills/agent-ops/scripts/test_agent_controls.py", False, ()),
    ("layout", ".agents/skills/quarto-theme/scripts/check_layout.py", True, ()),
    ("callouts", ".agents/skills/quarto-docs/scripts/check_callouts.py", True, ()),
    ("dom", ".agents/skills/agent-ops/scripts/check_dom_contracts.py", True, ()),
    ("size", ".agents/skills/agent-ops/scripts/check_skill_size.py", False, ()),
    ("ascii", ".agents/skills/quarto-docs/scripts/check_ascii_names.py", False, ()),
    ("links", ".agents/skills/quarto-docs/scripts/check_skill_links.py", False, ()),
    ("inline-code", ".agents/skills/agent-ops/scripts/check_inline_code.py", False, ()),
    ("docs", ".agents/skills/agent-ops/scripts/check_docs.py", False, ()),
    ("punctuation", ".agents/skills/agent-ops/scripts/check_punctuation.py", False, ()),
    ("tasks", ".agents/skills/agent-ops/scripts/check_task_matrix.py", False, ()),
    ("scaffold", ".agents/skills/python-tools/scripts/test_scaffold_projects.py", False, ()),
    ("kb", ".agents/skills/python-tools/scripts/check_health.py", False, ("--gate",)),
    ("kb-eval", ".agents/skills/python-tools/scripts/evaluator.py", False, ("--skip-latency",)),
    ("conflict", ".agents/skills/python-tools/scripts/test_conflict_detection.py", False, ()),
    ("vector-eq", ".agents/skills/python-tools/scripts/test_vector_index_equivalence.py", False, ()),
    ("vector-shard", ".agents/skills/python-tools/scripts/test_vector_sharding.py", False, ()),
]

PROFILE_CHECKS = {
    "fast": {
        "empty", "encoding", "agent-controls", "size", "ascii", "links",
        "inline-code", "docs", "punctuation", "tasks",
    },
    "book": {"layout", "callouts", "dom"},
    "knowledge": {"kb", "kb-eval", "conflict", "vector-eq", "vector-shard"},
    "python": {"scaffold"},
}

# 成功判据行：命中即认为该步通过，用于从大输出里挑出唯一有价值的一行
PASS_HINTS = ("PASS", "All examples compiled", "All key tokens", "OK: all internal",
              "无阻塞", "DOM contracts")
CHECK_LABELS = {
    "empty": "空文件",
    "encoding": "编码",
    "agent-controls": "Agent 控制",
    "layout": "布局",
    "callouts": "提示框",
    "dom": "页面结构",
    "size": "上下文体量",
    "ascii": "文件名",
    "links": "链接",
    "inline-code": "行内代码",
    "docs": "文档",
    "punctuation": "标点",
    "tasks": "任务矩阵",
    "scaffold": "脚手架",
    "kb": "知识库",
    "kb-eval": "知识库评测",
    "conflict": "冲突检测",
    "vector-eq": "向量等价",
    "vector-shard": "向量分片",
}
COMMAND_LABELS = {
    "kb-index": "知识库索引",
    "kb-check": "知识库检查",
    "kb-eval": "知识库评测",
    "kb-scale": "规模基准",
}


def display_check(item):
    """把内部检查名转换成中文状态文本。"""
    name, separator, detail = item.partition(":")
    label = CHECK_LABELS.get(name, name)
    return f"{label}（{detail}）" if separator else label


def display_command(label):
    """把内部子命令名转换成中文状态文本。"""
    return COMMAND_LABELS.get(label, label)


def checks_for_profile(profile):
    """返回指定 profile 的校验项；full 保持原有全部检查。"""
    if profile == "full":
        return CHECKS
    names = PROFILE_CHECKS[profile]
    return [item for item in CHECKS if item[0] in names]


def to_wsl_path(win_path):
    """把 Windows 绝对路径转成 WSL 可见路径：D:\\a\\b -> /mnt/d/a/b。"""
    s = str(win_path).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def run(argv, cwd=ROOT, env=None):
    """执行命令并捕获输出（bytes 手工解码，绕开 PowerShell 与 GBK 问题）。"""
    command = list(argv)
    if command and not Path(command[0]).is_file():
        command[0] = resolve_tool(command[0])
    child_env = dict(os.environ if env is None else env)
    if PY and Path(command[0]).resolve() == Path(PY).resolve():
        child_env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(command, cwd=str(cwd), env=child_env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    text = proc.stdout.decode("utf-8", errors="replace")
    return proc.returncode, text


def tail(text, n):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return lines[-n:]


def interpret(rc, text, verbose, label):
    """分级输出：成功一行、失败展开末尾若干行。"""
    if rc == 0:
        if verbose:
            print(text.rstrip())
        else:
            print(f"通过  {display_command(label)}")
        return 0
    print(f"失败  {display_command(label)}（退出码 {rc}）")
    for ln in tail(text, 60 if verbose else 12):
        print(f"      {ln}")
    return rc


def cmd_check(args):
    """运行指定 profile 的校验。默认只回一行总结。"""
    checks = checks_for_profile(args.profile)
    details, failed, reported, skipped = [], [], [], []
    kb_ready = True
    if any(name in {"kb", "kb-eval"} for name, *_rest in checks):
        rc = ensure_kb_index()
        if rc != 0:
            failed.append("kb:index")
            kb_ready = False
    for name, script, need_book, extra in checks:
        path = ROOT / script
        if not path.is_file():
            failed.append(f"{name}:脚本缺失")
            continue
        if name in {"kb", "kb-eval"} and not kb_ready:
            continue
        if need_book and not (ROOT / "_book").is_dir():
            if getattr(args, "require_book", False):
                failed.append(f"{name}:未渲染")
            else:
                skipped.append(f"{name}:未渲染")
            continue
        argv = [PY, str(path), *extra]
        if need_book:
            argv += ["--book-dir", "_book"]
        if name == "layout" and getattr(args, "require_browser", False):
            argv.append("--browser")
        if getattr(args, "strict", False) and name in {"punctuation", "docs"}:
            argv.append("--strict")
        rc, text = run(argv)
        if rc != 0:
            failed.append(name)
            if args.verbose:
                print(f"--- {name} ---")
                print(text.rstrip())
        else:
            if any(line.startswith("REPORT encoding") for line in text.splitlines()):
                reported.append(name)
            skip_line = next(
                (line.strip() for line in text.splitlines() if line.strip().startswith("SKIP ")),
                "",
            )
            if skip_line:
                if name == "layout" and getattr(args, "require_browser", False):
                    failed.append(f"{name}:{skip_line.removeprefix('SKIP ').strip()}")
                    continue
                skipped.append(f"{CHECK_LABELS.get(name, name)}：{skip_line.removeprefix('SKIP ').strip()}")
            last = next((ln for ln in reversed(text.splitlines())
                         if any(h in ln for h in PASS_HINTS)), "")
            details.append(
                f"{name}={skip_line or last.strip() or 'ok'}"
            )

    if not failed:
        suffix = f"；软报告 {','.join(CHECK_LABELS.get(name, name) for name in reported)}" if reported else ""
        if skipped:
            suffix += f"；跳过 {len(skipped)} 项"
            print(f"通过  检查（{args.profile}）：{len(checks)} 项已检查{suffix}")
        else:
            print(f"通过  检查（{args.profile}）：{len(checks)} 项全通过{suffix}")
        if args.verbose:
            for d in details:
                print(f"      {d}")
        return 0
    print(f"失败  检查（{args.profile}）：{', '.join(display_check(item) for item in failed)}")
    if not args.verbose:
        print("      提示：加 --verbose 查看失败项详情")
    return 1


def cmd_verify(args):
    """编译校验示例。Windows 自动调用 WSL，默认只回结论行以控制输出量。"""
    argv = [PY, str(ROOT / ".agents/skills/cpp-content/scripts/verify_examples.py")]
    note = ""
    if args.style:
        argv.append("--style")
    if args.changed:
        changed = changed_paths()
        if changed is None:
            note = "（全局配置或校验器有改动，已改为全量）"
        else:
            paths = relevant_cpp_paths(changed)
            if not paths:
                print("跳过  C++ 示例校验：没有相关改动")
                return 0
            argv += ["--paths", *paths]
    rc, text = run(argv)
    if args.verbose:
        print(text.rstrip())
        return rc
    if rc != 0:
        print(f"失败  C++ 示例校验{note}（退出码 {rc}）")
        keep = [ln for ln in text.splitlines()
                if ln.strip() and not ln.lstrip().startswith("===")]
        for ln in keep[-25:]:
            print(f"      {ln.rstrip()}")
        return rc
    print(f"通过  C++ 示例校验{note}")
    return 0


def changed_paths():
    """返回相对 HEAD 的工作区路径。全局 C++ 改动时返回 None。"""
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"], cwd=str(ROOT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    raw = result.stdout.decode("utf-8", errors="replace")
    paths = []
    items = raw.split("\0")
    index = 0
    while index < len(items):
        item = items[index]
        if not item or len(item) < 4:
            index += 1
            continue
        status = item[:2]
        path = item[3:].strip('"')
        if "R" in status or "C" in status:
            index += 1
        path = path.replace("\\", "/")
        if any(part in {"build", ".cache", ".tmp", "temp", ".quarto", "__pycache__"}
               for part in path.split("/")):
            index += 1
            continue
        paths.append(path)
        index += 1

    global_prefixes = (
        ".agents/skills/cpp-content/assets/config/",
        ".agents/skills/cpp-content/templates/",
        ".agents/skills/python-tools/scripts/scaffold/",
        ".agents/skills/cpp-content/scripts/",
    )
    global_files = {
        ".agents/skills/agent-ops/scripts/run.py",
        ".agents/skills/cpp-content/scripts/verify_examples.py",
    }
    if any(path.startswith(global_prefixes) or path in global_files for path in paths):
        return None
    return paths


def relevant_cpp_paths(paths):
    """筛出可交给 verify_examples.py 的 C++、CMake 和 QMD 文件。"""
    selected = []
    for path in paths:
        suffix = Path(path).suffix.lower()
        if (
            path.startswith("code/")
            and suffix in {".cpp", ".cc", ".cxx", ".h", ".hh", ".hpp"}
            and (ROOT / path).is_file()
        ):
            selected.append(path)
        elif (
            path.startswith("code/")
            and Path(path).name == "CMakeLists.txt"
            and (ROOT / path).is_file()
        ):
            selected.append(path)
        elif path.endswith(".qmd") and (ROOT / path).is_file():
            selected.append(path)
        elif (
            path.startswith(".agents/skills/cpp-content/references/cpp/")
            and path.endswith(".md")
            and (ROOT / path).is_file()
        ):
            selected.append(path)
    return selected


def cmd_render(args):
    """渲染 Book 后运行 book profile；浏览器矩阵只在 --require-browser 时执行。"""
    rc, text = run(["quarto", "render"] + (["--no-quartoignore"] if args.no_ignore else []))
    if rc != 0:
        print(f"失败  渲染（退出码 {rc}）")
        for ln in tail(text, 30):
            print(f"      {ln}")
        return rc
    err = [ln for ln in text.splitlines() if "WARNING" in ln or "ERROR" in ln]
    print(f"通过  渲染：警告或错误 {len(err)} 条")
    if not args.skip_check:
        args.profile = "book"
        args.require_book = True
        return cmd_check(args)
    return 0


def cmd_scope(args):
    argv = [PY, str(ROOT / ".agents/skills/agent-ops/scripts/scope.py")]
    if args.list:
        argv.append("--list")
    if args.verbose:
        argv.append("--verbose")
    if args.target:
        argv.append(args.target)
    rc, text = run(argv)
    print(text.rstrip())
    return rc


def cmd_build(args):
    """按需启动 WSL 运行章节构建，并生成 clangd 用的编译数据库。"""
    target = args.target.strip("/\\")
    script = ROOT / "code" / target / "build-and-run.sh"
    if not script.is_file():
        print(f"失败  构建：找不到 {script.relative_to(ROOT)}")
        return 1
    env_path = to_wsl_path(script.parent)
    rc, text = run(["wsl.exe", "bash", "-lc", f"cd '{env_path}' && bash build-and-run.sh"])
    if rc != 0:
        print(f"失败  构建 {target}（退出码 {rc}）")
        for ln in tail(text, 20):
            print(f"      {ln}")
        return rc
    print(f"通过  构建 {target}")
    if args.verbose:
        for ln in tail(text, 8):
            print(f"      {ln}")
    return 0


def cmd_status(args):
    """git 状态：按维护域与内容域归类，不推断改动归属。"""
    rc, text = run(["git", "status", "--porcelain"])
    maintenance, content = [], []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        body = ln[3:].split(" -> ")[-1].strip().strip('"')
        (maintenance if status_group(body) == "maintenance" else content).append(ln)
    print(f"维护域文件 {len(maintenance)} 项 / 内容与工程域 {len(content)} 项")
    if args.verbose or args.all:
        for ln in maintenance:
            print(f"  {ln}")
    if args.all:
        for ln in content:
            print(f"  (内容/工程) {ln}")
    return rc


def status_group(path):
    """按文件域归类 git 状态，不推断改动作者。"""
    maintenance_prefixes = (".agents/", "AGENTS.md", ".gitattributes", ".gitignore")
    return "maintenance" if path.startswith(maintenance_prefixes) else "content"


KB_INDEX_DB = "temp/knowledge-index/kb_index.sqlite"


def kb_script(name):
    """拼出 .agents/skills/python-tools/scripts/ 下的知识库脚本绝对路径。"""
    return str(ROOT / ".agents" / "skills" / "python-tools" / "scripts" / name)


def ensure_kb_index():
    """索引产物不入库（见 .gitignore），缺失时先全量重建，避免子命令空跑。"""
    if (ROOT / KB_INDEX_DB).is_file():
        return 0
    print("提示  知识库索引缺失，正在全量重建")
    rc, text = run([PY, kb_script("indexer.py"), "--rebuild"])
    if rc != 0:
        print(f"失败  知识库索引（退出码 {rc}）")
        for ln in tail(text, 12):
            print(f"      {ln}")
        return rc
    return rc


def cmd_kb_index(args):
    """重建或增量更新索引。"""
    argv = [PY, kb_script("indexer.py")]
    if args.rebuild:
        argv.append("--rebuild")
    rc, text = run(argv)
    return interpret(rc, text, args.verbose, "kb-index")


def cmd_kb_search(args):
    """检索知识库：retriever 已按预算输出，故直接透传结果。"""
    rc = ensure_kb_index()
    if rc != 0:
        return rc
    rc, text = run([PY, kb_script("retriever.py"), *args.rest])
    print(text.rstrip())
    return rc


def cmd_kb_check(args):
    """知识库健康度检查（结构 + 延迟）。"""
    rc = ensure_kb_index()
    if rc != 0:
        return rc
    argv = [PY, kb_script("check_health.py")]
    if args.gate:
        argv.append("--gate")
    if args.verbose:
        argv.append("--verbose")
    rc, text = run(argv)
    return interpret(rc, text, args.verbose, "kb-check")


def cmd_kb_eval(args):
    """标注集验收：Top-K 召回率与注入令牌，延迟由 kb-check 负责。"""
    rc = ensure_kb_index()
    if rc != 0:
        return rc
    argv = [PY, kb_script("evaluator.py"), "--topk", str(args.topk), "--skip-latency"]
    if args.verbose:
        argv.append("--verbose")
    rc, text = run(argv)
    return interpret(rc, text, args.verbose, "kb-eval")


def cmd_kb_scale(args):
    """规模基准：合成 Chunk 逐级测 P95，给出当前实现的可撑体量拐点。"""
    argv = [PY, kb_script("benchmark_scale.py"), "--sizes", args.sizes,
            "--repeats", str(args.repeats)]
    if args.verbose:
        argv.append("--verbose")
    rc, text = run(argv)
    return interpret(rc, text, args.verbose, "kb-scale")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if PY is None:
        print("失败  manifest 未提供可执行的 Python >= 3.12；请修复 .agents/manifest.json 的 mcp.command")
        return 1
    if sys.version_info < MIN_PYTHON:
        required = ".".join(map(str, MIN_PYTHON))
        print(f"失败  Python 需要 >= {required}，当前为 {sys.version.split()[0]}；请切换解释器")
        return 1
    configured = Path(PY).resolve()
    current = Path(sys.executable).resolve()
    if current != configured:
        print(
            "失败  run.py 必须由 manifest.mcp.command 指定的解释器执行；"
            f"当前={current}，配置={configured}"
        )
        return 1

    # 公共参数：用 parents 挂到每个子命令上，这样 --verbose 放前放后都能识别
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--verbose", action="store_true", help="展开完整原始输出")

    parser = argparse.ArgumentParser(description="agent 命令统一入口（默认 terse 输出）")
    subs = parser.add_subparsers(dest="cmd", required=True)

    p = subs.add_parser("check", parents=[common], help="一次跑完全部校验")
    p.add_argument("--strict", action="store_true",
                   help="把正文分号、链接间距等软规则升级为失败（作用于 punctuation 与 docs）")
    p.add_argument("--require-book", action="store_true",
                   help="缺少 _book/ 时让 layout/callouts/dom 失败，默认显示跳过")
    p.add_argument("--require-browser", action="store_true",
                   help="浏览器布局检查未执行时失败，默认显示跳过")
    p.add_argument("--profile", choices=("fast", "book", "knowledge", "python", "full"),
                   default="full", help="校验范围，默认 full")
    p = subs.add_parser("verify", parents=[common], help="编译校验 C++ 示例")
    p.add_argument("--style", action="store_true", help="追加 clang-format / clang-tidy")
    p.add_argument("--changed", action="store_true", help="只校验相对 HEAD 修改的 C++ 内容")
    p = subs.add_parser("render", parents=[common], help="渲染并自动校验")
    p.add_argument("--no-ignore", action="store_true", help="传给 quarto --no-quartoignore")
    p.add_argument("--skip-check", action="store_true", help="渲染后不跑校验")
    p.add_argument("--require-browser", action="store_true",
                   help="浏览器布局检查未执行时失败")
    p = subs.add_parser("scope", parents=[common], help="输出任务作用域清单")
    p.add_argument("target", nargs="?")
    p.add_argument("--list", action="store_true")
    p = subs.add_parser("build", parents=[common], help="WSL 内跑章节示例一键构建")
    p.add_argument("target")
    p = subs.add_parser("status", parents=[common], help="精简 git 状态")
    p.add_argument("--all", action="store_true", help="同时列出内容与工程域改动")
    p = subs.add_parser("kb-index", parents=[common], help="重建或增量更新知识库索引")
    p.add_argument("--rebuild", action="store_true", help="清空索引后全量重建")
    p = subs.add_parser("kb-search", parents=[common], help="知识库检索（参数透传 retriever）")
    p.add_argument("rest", nargs=argparse.REMAINDER, help="查询串与 retriever 参数（顺序任意）")
    p = subs.add_parser("kb-check", parents=[common], help="知识库健康度与延迟")
    p.add_argument("--gate", action="store_true", help="只把结构性问题视为失败")
    p = subs.add_parser("kb-eval", parents=[common], help="标注集召回率与预算验收")
    p.add_argument("--topk", type=int, default=5, help="召回评价的 K，默认 5")
    p = subs.add_parser("kb-scale", parents=[common], help="三层索引规模基准与 P95 拐点")
    p.add_argument("--sizes", default="1000,10000,50000,100000", help="逗号分隔的 Chunk 数")
    p.add_argument("--repeats", type=int, default=3, help="每级重复次数")

    args, extra = parser.parse_known_args()
    if args.cmd == "kb-search":
        # retriever 的参数表由 .agents/skills/python-tools/scripts/retriever.py 自己定义，本解析器只做统一入口，
        # 故按原始 argv 顺序整体接管 kb-search 之后的参数，避免 --toc 这类 flag 被
        # 本层吞掉后报 unrecognized arguments。--verbose 归本层使用，其余原样透传。
        tail = sys.argv[sys.argv.index("kb-search") + 1:]
        args.rest = [t for t in tail if t != "--verbose"]
    elif extra:
        parser.error("未识别的参数: " + " ".join(extra))
    handlers = {"check": cmd_check, "verify": cmd_verify, "render": cmd_render,
                "scope": cmd_scope, "build": cmd_build, "status": cmd_status,
                "kb-index": cmd_kb_index, "kb-search": cmd_kb_search,
                "kb-check": cmd_kb_check, "kb-eval": cmd_kb_eval,
                "kb-scale": cmd_kb_scale}
    try:
        return handlers[args.cmd](args)
    except ToolNotFound as exc:
        print(f"失败  {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
