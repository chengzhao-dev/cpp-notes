"""检查 skills 与 AGENTS.md 的行数是否越界：三层加载契约的体积护栏。

为什么需要它：省 token 的地基是「稳定前缀要短」。AGENTS.md 与 SKILL.md 每轮都被重读，
每多一行 ≈ 每轮多付一行；reference 过长则一次任务就读掉大量无关内容。本脚本把预算
固化成断言，越界即 FAIL，防止新框架被重新写胖。

预算（三层加载契约）：
  L0  AGENTS.md                     <= 45 行 且 <= 3400 字节
  L1  .cursor/skills/*/SKILL.md     <= 45 行 且 <= 3000 字节
  L2  .cursor/skills/*/references/**.md <= 160 行 且 <= 10000 字节
      （内聚的单一主题不硬拆：拆开会迫使一次读多份，反而更费 token）

为什么同时管字节：中文一行可密可疏，只按行数会被「写成密集长行」绕过；
真正决定成本的是字符量，故两个维度都要卡。

用法：python check_skill_size.py [--verbose]
退出码：0 = 全部在预算内；1 = 有文件越界。
"""
import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L0 = (ROOT / "AGENTS.md", 45, 3400, "L0 稳定前缀")
L1_GLOB = (".cursor/skills/*/SKILL.md", 45, 3000, "L1 任务路由")
L2_GLOB = (".cursor/skills/*/references/**/*.md", 160, 10000, "L2 原子知识")


def stat(path):
    """"返回 (行数, 字节数)。"""
    raw = io.open(path, encoding="utf-8", errors="ignore").read()
    return len(raw.splitlines()), len(raw.encode("utf-8"))


def scan(pattern, line_limit, byte_limit, tier):
    bad, total = [], 0
    for path in sorted(ROOT.glob(pattern)):
        n, b = stat(path)
        total += 1
        if n > line_limit:
            bad.append((tier, path.relative_to(ROOT).as_posix(), "%d 行 > %d" % (n, line_limit)))
        elif b > byte_limit:
            bad.append((tier, path.relative_to(ROOT).as_posix(), "%d 字节 > %d" % (b, byte_limit)))
    return bad, total


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="skills 体积护栏")
    ap.add_argument("--verbose", action="store_true", help="逐项列出文件与行数")
    args = ap.parse_args()

    bad = []
    n0, b0 = stat(L0[0])
    if n0 > L0[1]:
        bad.append((L0[3], "AGENTS.md", "%d 行 > %d" % (n0, L0[1])))
    elif b0 > L0[2]:
        bad.append((L0[3], "AGENTS.md", "%d 字节 > %d" % (b0, L0[2])))
    counts = [("AGENTS.md", n0, b0)]

    for pattern, line_limit, byte_limit, tier in (L1_GLOB, L2_GLOB):
        b, _t = scan(pattern, line_limit, byte_limit, tier)
        bad += b
        if args.verbose:
            for path in sorted(ROOT.glob(pattern)):
                n, sz = stat(path)
                counts.append((path.relative_to(ROOT).as_posix(), n, sz))

    if args.verbose:
        for name, n, sz in counts:
            print(f"  {n:>4} 行 {sz:>6} 字节  {name}")

    if bad:
        print(f"FAIL  skill-size 越界 {len(bad)} 项")
        for tier, name, why in bad:
            print(f"      {tier}  {name}  {why}")
        return 1
    print(f"PASS  skill-size  AGENTS.md={n0} 行/{b0} 字节；L1/L2 全在预算内")
    return 0


if __name__ == "__main__":
    sys.exit(main())