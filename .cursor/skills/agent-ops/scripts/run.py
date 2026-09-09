#!/usr/bin/env python3
"""agent 命令统一入口：把易踩坑的 Windows/PowerShell 调用包成稳定的单轮输出。

为什么需要它：省 token 的最大杠杆不是「少读文件」，而是「少几轮」。在 Windows 上
手写 PowerShell/cmd 命令常因引号与 GBK 编码失败，每次重试都把整段上下文与输出重付一遍；
渲染与校验的原始输出动辄上千行，全量回灌同样昂贵。本脚本用 Python 直接 subprocess
调用（不经 PowerShell 解析），并对输出做截断与分级：成功只回一行，失败才展开。

子命令：
  check   一次跑完全部产物/源码校验（默认 terse：仅一行结论）
  verify  编译校验 C++ 示例（Windows 自动经 WSL2；可 --changed 增量校验）
  render  渲染 Book 并自动跑产物校验（合并为 1 轮）
  scope   解析任务作用域，输出 UNIT/READ/DENY 清单
  build   在 WSL 中跑某章节示例的一键构建（按需启动默认 Ubuntu，供 clangd 生成编译数据库）
  status  精简 git 状态：默认折叠用户既有改动，只看本次相关
  kb-index  增量或全量重建知识库索引（knowledge/ -> temp/knowledge-index/）
  kb-search  知识库单次检索（透传 retriever 参数，如 --toc/--parent/--explain）
  kb-check  知识库健康度与检索延迟测量
  kb-eval   标注集召回率与 Token 预算验收
  kb-scale  三层索引的规模基准（P95 拐点，验证 100MB–1GB 目标）
通用参数：
  --verbose  展开全部原始输出（仅失败排查时使用）
退出码：透传被包装命令的退出码；0 = 成功。
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
RUNTIME_CONFIG = ROOT / ".cursor" / "skills" / "python-tools" / "assets" / "config" / "runtime.json"


class ToolNotFound(RuntimeError):
    """外部工具未找到。"""


def runtime_config():
    """读取本机运行时配置；配置缺失或损坏时交给后续搜索。"""
    try:
        return json.loads(RUNTIME_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def python_version(candidate):
    """返回解释器版本元组；无法执行时返回空值。"""
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
    """按固定路径优先、PATH 回退选择满足最低版本的 Python。"""
    config = runtime_config()
    candidates = [os.environ.get("CPP_MEMO_PYTHON"), config.get("python")]
    candidates.extend(shutil.which(name) for name in ("python", "python3"))
    candidates.append(sys.executable)
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
            return str(candidate)
    raise ToolNotFound(f"找不到工具 {name}；请配置 {env_name} 或安装后加入 PATH")

# 校验项：(名称, 脚本相对路径, 需要 _book 产物)
CHECKS = [
    ("empty", ".cursor/skills/agent-ops/scripts/check_empty.py", False),
    ("encoding", ".cursor/skills/agent-ops/scripts/check_encoding.py", False),
    ("agent-controls", ".cursor/skills/agent-ops/scripts/test_agent_controls.py", False),
    ("layout", ".cursor/skills/quarto-theme/scripts/check_layout.py", True),
    ("callouts", ".cursor/skills/quarto-docs/scripts/check_callouts.py", True),
    ("dom", ".cursor/skills/agent-ops/scripts/check_dom_contracts.py", True),
    ("size", ".cursor/skills/agent-ops/scripts/check_skill_size.py", False),
    ("ascii", ".cursor/skills/quarto-docs/scripts/check_ascii_names.py", False),
    ("links", ".cursor/skills/quarto-docs/scripts/check_skill_links.py", False),
    ("docs", ".cursor/skills/agent-ops/scripts/check_docs.py", False),
    ("conflict", ".cursor/skills/python-tools/scripts/test_conflict_detection.py", False),
    ("vector-eq", ".cursor/skills/python-tools/scripts/test_vector_index_equivalence.py", False),
    ("vector-shard", ".cursor/skills/python-tools/scripts/test_vector_sharding.py", False),
]

# 成功判据行：命中即认为该步通过，用于从大输出里挑出唯一有价值的一行
PASS_HINTS = ("PASS", "All examples compiled", "All key tokens", "OK: all internal",
              "无阻塞", "DOM contracts")


def to_wsl_path(win_path):
    """把 Windows 绝对路径转成 WSL 可见路径：D:\\a\\b -> /mnt/d/a/b。"""
    s = str(win_path).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def run(argv, cwd=ROOT, env=None):
    """执行命令并捕获输出（bytes 手工解码，绕开 PowerShell 与 GBK 问题）。"""
    command = list(argv)
    if command and not Path(command[0]).is_file():
        command[0] = resolve_tool(command[0])
    proc = subprocess.run(command, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
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
            key = next((ln for ln in reversed(text.splitlines())
                        if any(h in ln for h in PASS_HINTS)), "done")
            print(f"PASS  {label}  {key.strip()}")
        return 0
    print(f"FAIL  {label}  (exit={rc})")
    for ln in tail(text, 60 if verbose else 12):
        print(f"      {ln}")
    return rc


def cmd_check(args):
    """一次跑完全部校验；默认只回一行总结。"""
    details, failed, reported = [], [], []
    for name, script, need_book in CHECKS:
        path = ROOT / script
        if not path.is_file():
            failed.append(f"{name}:脚本缺失")
            continue
        if need_book and not (ROOT / "_book").is_dir():
            failed.append(f"{name}:未渲染")
            continue
        argv = [PY, str(path)]
        if need_book:
            argv += ["--book-dir", "_book"]
        rc, text = run(argv)
        if rc != 0:
            failed.append(name)
            if args.verbose:
                print(f"--- {name} ---")
                print(text.rstrip())
        else:
            if any(line.startswith("REPORT encoding") for line in text.splitlines()):
                reported.append(name)
            last = next((ln for ln in reversed(text.splitlines())
                         if any(h in ln for h in PASS_HINTS)), "")
            details.append(f"{name}={last.strip() or 'ok'}")

    if not failed:
        suffix = f"；软报告={','.join(reported)}" if reported else ""
        print(f"PASS  check {len(CHECKS)} 项全通过{suffix}")
        if args.verbose:
            for d in details:
                print(f"      {d}")
        return 0
    print(f"FAIL  check 未通过：{', '.join(failed)}")
    if not args.verbose:
        print("      提示：加 --verbose 查看失败项详情")
    return 1


def cmd_verify(args):
    """编译校验示例；Windows 自动调用 WSL，默认只回结论行以控制输出量。"""
    argv = [PY, str(ROOT / ".cursor/skills/cpp-content/scripts/verify_examples.py")]
    if args.style:
        argv.append("--style")
    if args.changed:
        changed = changed_paths()
        if changed is None:
            print("INFO  verify --changed  检测到全局 C++ 配置或校验器改动，改为全量校验")
        else:
            paths = relevant_cpp_paths(changed)
            if not paths:
                print("SKIP  verify --changed  没有修改的 C++ 源文件或内嵌示例")
                return 0
            argv += ["--paths", *paths]
    rc, text = run(argv)
    if args.verbose:
        print(text.rstrip())
        return rc
    # terse：保留失败行与最终结论，压掉逐个 compile 的流水
    keep = [ln for ln in text.splitlines()
            if ln.strip().startswith(("FAIL", "=== Phase", "All examples", "example(s) failed",
                                      "skip", "MISS", "no ", "未检测", "Windows："))]
    for ln in keep[-25:]:
        print(ln.rstrip())
    if rc == 0:
        print("PASS  verify 示例全部编译通过")
    return rc


def changed_paths():
    """返回相对 HEAD 的工作区路径；全局 C++ 改动时返回 None。"""
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"], cwd=str(ROOT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    raw = result.stdout.decode("utf-8", errors="replace")
    paths = []
    for item in raw.split("\0"):
        if not item or len(item) < 4:
            continue
        path = item[3:].split(" -> ")[-1].strip('"')
        path = path.replace("\\", "/")
        if any(part in {"build", ".cache", ".tmp", ".quarto", "__pycache__"}
               for part in path.split("/")):
            continue
        paths.append(path)

    global_prefixes = (
        ".cursor/skills/cpp-content/assets/config/",
        ".cursor/skills/python-tools/scripts/scaffold/",
        ".cursor/skills/cpp-content/scripts/",
    )
    global_files = {
        ".cursor/skills/agent-ops/scripts/run.py",
        ".cursor/skills/cpp-content/scripts/verify_examples.py",
    }
    if any(path.startswith(global_prefixes) or path in global_files for path in paths):
        return None
    return paths


def relevant_cpp_paths(paths):
    """筛出可交给 verify_examples.py 的 C++ 文件和 QMD 文件。"""
    selected = []
    for path in paths:
        if path.endswith(".cpp") and path.startswith("code/") and (ROOT / path).is_file():
            selected.append(path)
        elif path.endswith(".qmd") and (ROOT / path).is_file():
            selected.append(path)
    return selected


def cmd_render(args):
    """渲染 Book（改 .cursor/skills/quarto-theme/assets/theme/ 或 _quarto.yml 会整本重渲染，故单独提示），成功后跑 check。"""
    if not args.quiet_warn and (ROOT / "handbook").is_dir():
        pass  # 渲染代价由调用方自行声明；此处只做，不劝说
    rc, text = run(["quarto", "render"] + (["--no-quartoignore"] if args.no_ignore else []))
    if rc != 0:
        print(f"FAIL  quarto render (exit={rc})")
        for ln in tail(text, 30):
            print(f"      {ln}")
        return rc
    err = [ln for ln in text.splitlines() if "WARNING" in ln or "ERROR" in ln]
    print(f"PASS  render  警告/错误行数={len(err)}")
    for ln in err[:10]:
        print(f"      {ln}")
    if not args.skip_check:
        return cmd_check(args)
    return 0


def cmd_scope(args):
    argv = [PY, str(ROOT / ".cursor/skills/agent-ops/scripts/scope.py")]
    if args.list:
        argv.append("--list")
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
        print(f"FAIL  build  找不到 {script.relative_to(ROOT)}")
        return 1
    env_path = to_wsl_path(script.parent)
    rc, text = run(["wsl.exe", "bash", "-lc", f"cd '{env_path}' && bash build-and-run.sh"])
    if rc != 0:
        print(f"FAIL  build  {target} (exit={rc})")
        for ln in tail(text, 20):
            print(f"      {ln}")
        return rc
    print(f"PASS  build  {target}")
    if args.verbose:
        for ln in tail(text, 8):
            print(f"      {ln}")
    return 0


def cmd_status(args):
    """git 状态：区分「本次 agent 改动」与「用户既有未提交改动」。"""
    rc, text = run(["git", "status", "--porcelain"])
    agent_prefixes = (".cursor/skills/agent-ops/scripts/", "operations/", ".cursor/skills/",
                      ".config/", ".cursor/skills/quarto-theme/assets/theme/", "",
                      "_quarto.yml", "AGENTS.md")
    mine, theirs = [], []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        body = ln[3:].split(" -> ")[-1].strip().strip('"')
        (mine if body.startswith(agent_prefixes) else theirs).append(ln)
    print(f"agent 域文件 {len(mine)} 项 / 其它改动 {len(theirs)} 项")
    for ln in mine:
        print(f"  {ln}")
    if args.all:
        for ln in theirs:
            print(f"  (其它) {ln}")
    return rc


KB_INDEX_DB = "temp/knowledge-index/kb_index.sqlite"


def kb_script(name):
    """拼出 .cursor/skills/python-tools/scripts/ 下的知识库脚本绝对路径。"""
    return str(ROOT / ".cursor" / "skills" / "python-tools" / "scripts" / name)


def ensure_kb_index():
    """索引产物不入库（见 .gitignore），缺失时先全量重建，避免子命令空跑。"""
    if (ROOT / KB_INDEX_DB).is_file():
        return 0
    print("INFO  知识库索引缺失，先执行一次全量重建")
    rc, text = run([PY, kb_script("indexer.py"), "--rebuild"])
    print(text.rstrip())
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
    """标注集验收：Top-K 召回率、注入令牌与延迟。"""
    rc = ensure_kb_index()
    if rc != 0:
        return rc
    argv = [PY, kb_script("evaluator.py"), "--topk", str(args.topk)]
    if args.gate:
        argv.append("--gate")
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
        print("FAIL  找不到满足 Python >= 3.12 的解释器；请安装 Python 或设置 CPP_MEMO_PYTHON")
        return 1
    if Path(PY).resolve() != Path(sys.executable).resolve():
        os.execv(PY, [PY, str(Path(__file__).resolve()), *sys.argv[1:]])
    if sys.version_info < MIN_PYTHON:
        required = ".".join(map(str, MIN_PYTHON))
        print(f"FAIL  Python 需要 >= {required}，当前为 {sys.version.split()[0]}；请切换解释器")
        return 1

    # 公共参数：用 parents 挂到每个子命令上，这样 --verbose 放前放后都能识别
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--verbose", action="store_true", help="展开完整原始输出")

    parser = argparse.ArgumentParser(description="agent 命令统一入口（默认 terse 输出）")
    subs = parser.add_subparsers(dest="cmd", required=True)

    subs.add_parser("check", parents=[common], help="一次跑完全部校验")
    p = subs.add_parser("verify", parents=[common], help="编译校验 C++ 示例")
    p.add_argument("--style", action="store_true", help="追加 clang-format / clang-tidy")
    p.add_argument("--changed", action="store_true", help="只校验相对 HEAD 修改的 C++ 内容")
    p = subs.add_parser("render", parents=[common], help="渲染并自动校验")
    p.add_argument("--no-ignore", action="store_true", help="传给 quarto --no-quartoignore")
    p.add_argument("--skip-check", action="store_true", help="渲染后不跑校验")
    p.add_argument("--quiet-warn", action="store_true", help="不提示整本重渲染代价")
    p = subs.add_parser("scope", parents=[common], help="输出任务作用域清单")
    p.add_argument("target", nargs="?")
    p.add_argument("--list", action="store_true")
    p = subs.add_parser("build", parents=[common], help="WSL 内跑章节示例一键构建")
    p.add_argument("target")
    p = subs.add_parser("status", parents=[common], help="精简 git 状态")
    p.add_argument("--all", action="store_true", help="同时列出用户既有改动")
    p = subs.add_parser("kb-index", parents=[common], help="重建或增量更新知识库索引")
    p.add_argument("--rebuild", action="store_true", help="清空索引后全量重建")
    p = subs.add_parser("kb-search", parents=[common], help="知识库检索（参数透传 retriever）")
    p.add_argument("rest", nargs=argparse.REMAINDER, help="查询串与 retriever 参数（顺序任意）")
    p = subs.add_parser("kb-check", parents=[common], help="知识库健康度与延迟")
    p.add_argument("--gate", action="store_true", help="只把结构性问题视为失败")
    p = subs.add_parser("kb-eval", parents=[common], help="标注集召回率与预算验收")
    p.add_argument("--topk", type=int, default=5, help="召回评价的 K，默认 5")
    p.add_argument("--gate", action="store_true", help="不卡延迟（延迟由 kb-check 负责）")
    p = subs.add_parser("kb-scale", parents=[common], help="三层索引规模基准与 P95 拐点")
    p.add_argument("--sizes", default="1000,10000,50000,100000", help="逗号分隔的 Chunk 数")
    p.add_argument("--repeats", type=int, default=3, help="每级重复次数")

    args, extra = parser.parse_known_args()
    if args.cmd == "kb-search":
        # retriever 的参数表由 .cursor/skills/python-tools/scripts/retriever.py 自己定义，本解析器只做统一入口，
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
        print(f"FAIL  {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
