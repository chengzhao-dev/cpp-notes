#!/usr/bin/env python3
"""校验关键设计令牌与组件选择器是否进入渲染产物（_book）。

用单次字面匹配（子串查找）+ 计数，不对压缩后大 CSS 做宽模式扫描。
规范出处：.opencode/skills/quarto-theme/references/theme-structure.md。

用法：python check_layout.py [--book-dir _book]
退出码：0 = 关键令牌全部存在；1 = 有缺失。
"""

import argparse
import sys
from pathlib import Path

# 与 references/design-tokens.md / theme-structure.md 的令牌保持同步
CHECKS = [
    ("light body token #201d1d", "--body-color: #201d1d"),
    ("light primary-green #1f883d", "#1f883d"),
    ("light navbar page-bg token", "--navbar-bg: #fdfcfc"),
    ("dark navbar page-bg token", "--navbar-bg: #131010"),
    ("body line-height 1.6875", "line-height: 1.6875"),
    ("accent green dot #2da44e", "#2da44e"),
    ("dark page #131010", "#131010"),
    ("dark body #e8e6e3", "#e8e6e3"),
    ("dark link #4da3ff", "#4da3ff"),
    ("dark primary-green #238636", "#238636"),
    ("best-practice callout", "callout-best-practice"),
    ("key-insight callout", "callout-key-insight"),
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

    # 每个文件只读一次，逐令牌做子串匹配
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
