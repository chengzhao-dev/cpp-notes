#!/usr/bin/env python3
"""agent 命令统一入口：把易踩坑的 Windows/PowerShell 调用包成稳定的单轮输出。

为什么需要它：省 token 的最大杠杆不是「少读文件」，而是「少几轮」。在 Windows 上
手写 PowerShell/cmd 命令常因引号与 GBK 编码失败，每次重试都把整段上下文与输出重付一遍；
渲染与校验的原始输出动辄上千行，全量回灌同样昂贵。本脚本用 Python 直接 subprocess
调用（不经 PowerShell 解析），并对输出做截断与分级：成功只回一行，失败才展开。

子命令：
  check   一次跑完全部产物/源码校验（默认 terse：仅一行结论）
  verify  编译校验 C++ 示例（可 --style 追加 clang-format/tidy）
  render  渲染 Book 并自动跑产物校验（合并为 1 轮）
  scope   解析任务作用域，输出 UNIT/READ/DENY 清单
  build   在 WSL 中跑某章节示例的一键构建（供 clangd 生成编译数据库）
  status  精简 git 状态：默认折叠用户既有改动，只看本次相关
通用参数：
  --verbose  展开全部原始输出（仅失败排查时使用）
退出码：透传被包装命令的退出码；0 = 成功。
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable

# 校验项：(名称, 脚本相对路径, 需要 _book 产物)
CHECKS = [
    ("layout", ".cursor/skills/quarto-theme/scripts/check_layout.py", True),
    ("callouts", ".cursor/skills/quarto-docs/scripts/check_callouts.py", True),
    ("dom", "scripts/agent/check_dom_contracts.py", True),
    ("ascii", ".cursor/skills/quarto-docs/scripts/check_ascii_names.py", False),
    ("links", ".cursor/skills/quarto-docs/scripts/check_skill_links.py", False),
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
    proc = subprocess.run(argv, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
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
    details, failed = [], []
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
            last = next((ln for ln in reversed(text.splitlines())
                         if any(h in ln for h in PASS_HINTS)), "")
            details.append(f"{name}={last.strip() or 'ok'}")

    if not failed:
        print(f"PASS  check {len(CHECKS)} 项全通过")
        if args.verbose:
            for d in details:
                print(f"      {d}")
        return 0
    print(f"FAIL  check 未通过：{', '.join(failed)}")
    if not args.verbose:
        print("      提示：加 --verbose 查看失败项详情")
    return 1


def cmd_verify(args):
    """编译校验示例（阶段多、输出长，故默认只回结论行）。"""
    argv = [PY, str(ROOT / ".cursor/skills/cpp-content/scripts/verify_examples.py")]
    if args.style:
        argv.append("--style")
    rc, text = run(argv)
    if args.verbose:
        print(text.rstrip())
        return rc
    # terse：保留失败行与最终结论，压掉逐个 compile 的流水
    keep = [ln for ln in text.splitlines()
            if ln.strip().startswith(("FAIL", "=== Phase", "All examples", "example(s) failed",
                                      "skip", "MISS", "no "))]
    for ln in keep[-25:]:
        print(ln.rstrip())
    if rc == 0:
        print("PASS  verify 示例全部编译通过")
    return rc


def cmd_render(args):
    """渲染 Book（改 theme/ 或 _quarto.yml 会整本重渲染，故单独提示），成功后跑 check。"""
    if not args.quiet_warn and (ROOT / "theme").is_dir():
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
    argv = [PY, str(ROOT / "scripts/agent/scope.py")]
    if args.list:
        argv.append("--list")
    if args.target:
        argv.append(args.target)
    rc, text = run(argv)
    print(text.rstrip())
    return rc


def cmd_build(args):
    """在 WSL 里跑章节示例的一键构建，顺带生成 clangd 用的编译数据库。"""
    target = args.target.strip("/\\")
    script = ROOT / "code" / target / "build-and-run.sh"
    if not script.is_file():
        print(f"FAIL  build  找不到 {script.relative_to(ROOT)}")
        return 1
    env_path = to_wsl_path(script.parent)
    rc, text = run(["wsl", "bash", "-lc", f"cd '{env_path}' && bash build-and-run.sh"])
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
    agent_prefixes = ("scripts/agent/", "docs/agent/", ".cursor/skills/",
                      ".clangd", ".clang-format", ".editorconfig", ".vscode/",
                      "theme/", "_quarto.yml", "AGENTS.md")
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


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="agent 命令统一入口（默认 terse 输出）")
    parser.add_argument("--verbose", action="store_true", help="展开完整原始输出")
    subs = parser.add_subparsers(dest="cmd", required=True)

    subs.add_parser("check", help="一次跑完全部校验")
    p = subs.add_parser("verify", help="编译校验 C++ 示例")
    p.add_argument("--style", action="store_true", help="追加 clang-format / clang-tidy")
    p = subs.add_parser("render", help="渲染并自动校验")
    p.add_argument("--no-ignore", action="store_true", help="传给 quarto --no-quartoignore")
    p.add_argument("--skip-check", action="store_true", help="渲染后不跑校验")
    p.add_argument("--quiet-warn", action="store_true", help="不提示整本重渲染代价")
    p = subs.add_parser("scope", help="输出任务作用域清单")
    p.add_argument("target", nargs="?")
    p.add_argument("--list", action="store_true")
    p = subs.add_parser("build", help="WSL 内跑章节示例一键构建")
    p.add_argument("target")
    p = subs.add_parser("status", help="精简 git 状态")
    p.add_argument("--all", action="store_true", help="同时列出用户既有改动")

    args = parser.parse_args()
    handlers = {"check": cmd_check, "verify": cmd_verify, "render": cmd_render,
                "scope": cmd_scope, "build": cmd_build, "status": cmd_status}
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())