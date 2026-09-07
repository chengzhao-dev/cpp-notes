"""检查 skills 与 AGENTS.md 的体量是否越界：三层加载契约的体积护栏。

为什么需要它：省 token 的地基是「稳定前缀要短」。AGENTS.md 与 SKILL.md 每轮都被重读，
reference 过长则一次任务就读掉大量无关内容。本脚本把预算固化成断言，越界即 FAIL。

为什么按字符而非字节：厂商给出的上限都是字符数，不是字节数。
  - Agent Skills 规范：name <= 64 characters，description <= 1024 characters。
  - OpenAI Codex：初始 skills 列表最多占上下文 2%，上下文未知时按 8000 characters 封顶。
  - Claude：skill listing 里 description 与 when_to_use 合计在 1536 characters 截断，
    SKILL.md 正文建议 < 5000 tokens。
字符数对中文是更好的 token 代理（一个汉字约一个 token）；按 UTF-8 字节会把中文多算约
三倍，迫使作者删掉必要内容来「过线」。因此 L1/L2 以字符为主，字节只用在厂商明确按字节
定义的 L0（project_doc_max_bytes = 65536）。中文没有厂商专属上限，下列数值取自上述通用
字符预算并按本项目实测余量收敛。

预算（三层加载契约）：
  L0  AGENTS.md                          <= 65536 字节（OpenAI project_doc_max_bytes）
  L1  .cursor/skills/*/SKILL.md          <= 45 行 且 <= 3000 字符
      front matter：name <= 64 字符、description <= 1024 字符
      全部 skill 的 name + description <= 8000 字符（Codex 列表预算）
  L2  .cursor/skills/*/references/**.md  <= 160 行 且 <= 6000 字符
      （内聚的单一主题不硬拆：拆开会迫使一次读多份，反而更费 token）

用法：python check_skill_size.py [--verbose]
退出码：0 = 全部在预算内；1 = 有文件越界。
"""
import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L0_BYTE_LIMIT = 65536
L1 = (".cursor/skills/*/SKILL.md", 45, 3000, "L1 任务路由")
L2 = (".cursor/skills/*/references/**/*.md", 160, 6000, "L2 原子知识")
NAME_CHAR_LIMIT = 64
DESCRIPTION_CHAR_LIMIT = 1024
LISTING_CHAR_LIMIT = 8000

FIELD_RE = re.compile(r"(?m)^(name|description):\s*(.*?)\s*$")


def read(path):
    return io.open(path, encoding="utf-8", errors="ignore").read()


def stat(path):
    """"返回 (行数, 字符数, 字节数)。"""
    raw = read(path)
    return len(raw.splitlines()), len(raw), len(raw.encode("utf-8"))


def front_fields(path):
    """取出 SKILL.md front matter 里的 name 与 description。"""
    raw = read(path)
    if not raw.startswith("---"):
        return {}
    end = raw.find("\n---", 3)
    if end < 0:
        return {}
    return dict(FIELD_RE.findall(raw[:end]))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="skills 体积护栏")
    ap.add_argument("--verbose", action="store_true", help="逐项列出文件与字符数")
    args = ap.parse_args()

    bad = []
    rows = []

    n0, c0, b0 = stat(ROOT / "AGENTS.md")
    if b0 > L0_BYTE_LIMIT:
        bad.append(("L0 稳定前缀", "AGENTS.md", "%d 字节 > %d" % (b0, L0_BYTE_LIMIT)))
    rows.append(("AGENTS.md", n0, c0))

    listing = 0
    for pattern, line_limit, char_limit, tier in (L1, L2):
        for path in sorted(ROOT.glob(pattern)):
            n, c, _b = stat(path)
            rel = path.relative_to(ROOT).as_posix()
            rows.append((rel, n, c))
            if n > line_limit:
                bad.append((tier, rel, "%d 行 > %d" % (n, line_limit)))
            elif c > char_limit:
                bad.append((tier, rel, "%d 字符 > %d" % (c, char_limit)))
            if tier.startswith("L1"):
                fields = front_fields(path)
                name = fields.get("name", "")
                desc = fields.get("description", "")
                listing += len(name) + len(desc)
                if not name or not desc:
                    bad.append((tier, rel, "front matter 缺少 name 或 description"))
                if len(name) > NAME_CHAR_LIMIT:
                    bad.append((tier, rel, "name %d 字符 > %d" % (len(name), NAME_CHAR_LIMIT)))
                if len(desc) > DESCRIPTION_CHAR_LIMIT:
                    bad.append(
                        (tier, rel, "description %d 字符 > %d" % (len(desc), DESCRIPTION_CHAR_LIMIT))
                    )

    if listing > LISTING_CHAR_LIMIT:
        bad.append(
            (
                "L1 列表预算",
                "全部 SKILL.md",
                "name+description %d 字符 > %d" % (listing, LISTING_CHAR_LIMIT),
            )
        )

    if args.verbose:
        for rel, n, c in rows:
            print(f"  {n:>4} 行 {c:>6} 字符  {rel}")

    if bad:
        print(f"FAIL  skill-size 越界 {len(bad)} 项")
        for tier, name, why in bad:
            print(f"      {tier}  {name}  {why}")
        return 1
    skills = len(list(ROOT.glob(L1[0])))
    refs = len(list(ROOT.glob(L2[0])))
    print(
        f"PASS  skill-size  AGENTS.md={n0} 行/{b0} 字节；"
        f"{skills} 个 L1、{refs} 个 L2 在字符预算内；列表 {listing}/{LISTING_CHAR_LIMIT} 字符"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())