#!/usr/bin/env python3
"""校验关键设计令牌与组件选择器是否进入渲染产物（_book）。

用单次字面匹配（子串查找）+ 计数，不对压缩后大 CSS 做宽模式扫描。
规范出处：.cursor/skills/quarto-theme/references/design-tokens.md。

用法：python check_layout.py [--book-dir _book]
退出码：0 = 关键令牌全部存在；1 = 有缺失。
"""

import argparse
import sys
from pathlib import Path

# 与 references/design-tokens.md / theme/css/tokens.css 保持同步
CHECKS = [
    ("light body token #171717", "--body-color: #171717"),
    ("light accent orange #F54E00", "#F54E00"),
    ("light navbar page-bg token", "--navbar-bg: #FFFFFF"),
    ("dark navbar page-bg token", "--navbar-bg: #0A0A0A"),
    ("body line-height 1.625", "line-height: 1.625"),
    ("accent dot token", "--dot-accent"),
    ("dark page #0A0A0A", "#0A0A0A"),
    ("dark body #EDEDED", "#EDEDED"),
    ("dark link #FF6A1A", "#FF6A1A"),
    ("callout note border light", "--callout-note-border: #2563EB"),
    # callout 断言只测内置 5 类：自定义 .callout-* 类会被 Quarto 丢弃（见 pitfalls.md #12）
    ("callout tip (best-practice semantics)", "--callout-tip-border"),
    ("callout warning (key-insight semantics)", "--callout-warning-border"),
    ("callout important (deep-dive semantics)", "--callout-important-border"),
]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-dir", default="_book", help="渲染产物目录（默认 _book）")
    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    if not book_dir.is_dir():
        print(f"BookDir not found: {book_dir}. Run 'quarto render' first.")
        return 1

    css_texts = [
        p.read_text(encoding="utf-8", errors="ignore")
        for p in sorted(book_dir.rglob("*.css"))
    ]

    fail = 0
    for name, pattern in CHECKS:
        found = any(pattern in text for text in css_texts)
        mark = "OK  " if found else "MISS"
        print(f"  {mark} {name}  ({pattern})")
        if not found:
            fail += 1

    print()
    if fail == 0:
        print("All key tokens/selectors present.")
        return 0
    print(f"{fail} token(s) missing; check theme/css/*.css and the SASS cache.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
