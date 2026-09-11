#!/usr/bin/env python3
"""校验两章的排版与密度闸门（布局回归）。

为什么需要它：三栏 grid 压缩、同特异 CSS 覆盖、CJK 折行点都只在浏览器里有最终答案，
读源文件测不出来。本脚本把 knowledge/quarto-docs/writing/typography-density-pattern.md
里的阈值变成断言，改 grid、改缩进、改文案之后由 run.py check 判定，不靠人工目视维持。

口径（唯一出处在同级 measure_pages.mjs）：
  盒子 = 代码块 / 表格 / 提示框 / 引用块 / 图表容器，只算最外层；
  文字带 = 盒子之外的 p 与 li；节 = 正文的直接子 section（一个 ## 一节）。

断言分两组：
  T1 计算样式与几何：1280 与 1100 两档视口，由 measure_pages.mjs 测量后在此断言。
  T2 锚点：全仓 .qmd 里的 `#锚点` 引用（含同页引用）必须能在 _book 产物中找到同名 id。

用法：python check_typography.py [--book-dir _book] [--verbose]
退出码：0 = 全部通过；1 = 有断言失败；2 = 产物目录不存在或测量器不可用。
闸门：1100 档正文 < 540px 或目录仍折行时，按计划把 _quarto.yml 的 margin-width
      由 256px 降回 224px 复测，不要再压 sidebar-width 或 --toc-indent。
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKIP_DIRS = {".git", "_book", ".quarto", "build", "node_modules", ".cache", ".tmp", "temp", "__pycache__"}
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "python-tools" / "scripts"))
from temp_paths import temp_dir  # noqa: E402
MEASURE = Path(__file__).resolve().parent / "measure_pages.mjs"

# 阈值出处见 typography-density-pattern.md；改数值必须同时改那份知识文件。
WIDTH_FLOOR = {1280: 640, 1100: 540}        # 正文段落实测宽度下限（px）
# 当前正文与主题间距的实测上限，用于捕获后续意外增长。
HEIGHT_CEIL = {"setup-wsl2": 4300, "first-program": 5100}   # 正文容器高上限（1280 档）
RATIO_FLOOR = 2.4                           # 文字带 / 盒子
MAX_CONSECUTIVE_BOXES = 1                   # 相邻盒子处数
MAX_BOXES_PER_SECTION = 2                   # 单个 ## 内盒子数
TOC_ITEM_MAX_HEIGHT = 26                    # 目录条目单行上限（px）
PAGES = {
    "setup": "content/getting-started/setup-wsl2.html",
    "first-program": "content/getting-started/first-program.html",
}
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(\s*([^)\s]+)\s*\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def resolve_node():
    """按 CPP_MEMO_NODE、PATH 顺序解析 node；缺失时返回 None。"""
    for candidate in (os.environ.get("CPP_MEMO_NODE"), shutil.which("node")):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    return None


def resolve_playwright_root():
    """找含 playwright 的 node_modules：CPP_MEMO_NODE_PATH → NODE_PATH → 自带 runtime。"""
    def has_playwright(directory):
        return directory and (Path(directory) / "playwright" / "index.js").is_file()

    for candidate in (os.environ.get("CPP_MEMO_NODE_PATH"), os.environ.get("NODE_PATH")):
        if has_playwright(candidate):
            return candidate
    cache = Path.home() / ".cache" / "codex-runtimes"
    if cache.is_dir():
        for candidate in sorted(cache.glob("*/dependencies/*/node_modules")):
            if has_playwright(candidate):
                return str(candidate)
    return None


def measure(book_dir, verbose):
    """跑浏览器测量器，返回解析后的指标；运行时不可用时返回 None。"""
    node = resolve_node()
    pw_root = resolve_playwright_root()
    if not node or not pw_root or not MEASURE.is_file():
        print("MISS 测量器不可用：需要 node 与 playwright（可设 CPP_MEMO_NODE / CPP_MEMO_NODE_PATH）")
        print(f"      node={node or '无'} NODE_PATH={pw_root or '无'} 测量脚本={MEASURE.name}")
        return None
    env = dict(os.environ, NODE_PATH=pw_root, PYTHONIOENCODING="utf-8")
    runtime = temp_dir("runtime")
    out = runtime / "measure.json"
    argv = [node, str(MEASURE), "--book-dir", str(book_dir), "--out", str(out)]
    proc = subprocess.run(argv, cwd=str(ROOT), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = proc.stdout.decode("utf-8", errors="replace")
    if proc.returncode != 0 or not out.is_file():
        print(f"MISS 测量失败（exit={proc.returncode}）")
        if verbose or text.strip():
            for line in text.splitlines()[-12:]:
                print("      " + line)
        return None
    return json.loads(out.read_text(encoding="utf-8"))


def check_measured(metrics):
    """按两档视口断言计算样式与几何，返回失败清单。"""
    failures = []
    for width_text, pages in metrics["viewports"].items():
        width = int(width_text)
        for page_id, data in pages.items():
            label = f"{page_id}@{width}"
            source_name = PAGES[page_id].rsplit("/", 1)[-1].replace(".html", "")

            for block in data["languageBlocks"]:
                if block["preBorderWidth"] != 0:
                    failures.append(f"{label}: 语言块内层 pre 边框 {block['preBorderWidth']}px，应为 0（框中框）")
                    break
            for block in data["languageBlocks"]:
                if block["divBorderWidth"] != 1:
                    failures.append(f"{label}: div.sourceCode 边框 {block['divBorderWidth']}px，应为 1")
                    break
            wraps = {block["codeWhiteSpace"] for block in data["languageBlocks"]} | {
                block["codeWhiteSpace"] for block in data["barePres"]}
            if wraps - {"pre-wrap"}:
                failures.append(f"{label}: 代码 white-space={sorted(wraps)}，wrap 语义被覆盖")

            floor = WIDTH_FLOOR.get(width)
            if floor and data["paragraphWidth"] < floor:
                failures.append(f"{label}: 正文段落宽 {data['paragraphWidth']}px < {floor}px（触发 margin-width 闸门）")

            wrapped = [item for item in data["tocItems"] if item["height"] > TOC_ITEM_MAX_HEIGHT]
            if wrapped:
                titles = "、".join(item["text"][:18] for item in wrapped[:3])
                failures.append(f"{label}: 目录折行 {len(wrapped)} 项（最高 {max(i['height'] for i in wrapped)}px）：{titles}")

            scrolled = [item for item in data["overflow"] if not item["scrolls"]]
            if scrolled:
                first = scrolled[0]
                failures.append(
                    f"{label}: {len(scrolled)} 处横向溢出，首个 {first['tag']}.{first['classes'][:24]} "
                    f"{first['scrollWidth']}>{first['clientWidth']}"
                )

            boxes, bands = data["boxCount"], data["textBandCount"]
            ratio = bands / boxes if boxes else float("inf")
            if ratio < RATIO_FLOOR:
                failures.append(f"{label}: 文字带/盒子 {ratio:.2f} < {RATIO_FLOOR}（{bands} 带 / {boxes} 盒）")
            if data["consecutiveBoxes"] > MAX_CONSECUTIVE_BOXES:
                failures.append(f"{label}: 连续盒子 {data['consecutiveBoxes']} 处 > {MAX_CONSECUTIVE_BOXES}")
            over = [item for item in data["boxesPerSection"] if item["boxes"] > MAX_BOXES_PER_SECTION]
            for item in over:
                failures.append(f"{label}: 「{item['title'][:20]}」内 {item['boxes']} 个盒子 > {MAX_BOXES_PER_SECTION}")
            ceil = HEIGHT_CEIL.get(source_name)
            if ceil and width == 1280 and data["contentHeight"] > ceil:
                failures.append(f"{label}: 正文容器高 {data['contentHeight']}px > {ceil}px")
    return failures


def qmd_sources():
    paths = [ROOT / "index.qmd"]
    base = ROOT / "content"
    if base.is_dir():
        paths.extend(base.rglob("*.qmd"))
    return sorted(p for p in paths if p.is_file())


def check_anchors(book_dir):
    """断言两章及全部 .qmd 里的锚点引用能在产物中解析。"""
    failures = []
    total = 0
    cache = {}
    for path in qmd_sources():
        rel = path.relative_to(ROOT).as_posix()
        in_fence = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                if "#" not in target or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                    continue
                file_part, anchor = target.split("#", 1)
                if not anchor or anchor.startswith("cb"):
                    continue
                source_html = path.with_suffix(".html").relative_to(ROOT).as_posix()
                if file_part:
                    resolved = (path.parent / file_part).resolve()
                    if resolved.suffix != ".html":
                        resolved = resolved.with_suffix(".html")
                    try:
                        source_html = resolved.relative_to(ROOT).as_posix()
                    except ValueError:
                        failures.append(f"{rel}:{number}: 锚点目标越出仓库：{target}")
                        continue
                product = book_dir / source_html
                if not product.is_file():
                    failures.append(f"{rel}:{number}: 锚点目标页未渲染：{source_html}")
                    continue
                key = str(product)
                if key not in cache:
                    cache[key] = set(re.findall(r'\bid="([^"]+)"', product.read_text(encoding="utf-8", errors="ignore")))
                total += 1
                if urllib.parse.unquote(anchor) not in cache[key]:
                    failures.append(f"{rel}:{number}: 锚点无法解析：{target}")
    return failures, total


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-dir", default="_book", help="渲染产物目录（默认 _book）")
    parser.add_argument("--verbose", action="store_true", help="展开逐项指标")
    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    if not book_dir.is_dir():
        print(f"MISS 产物目录不存在：{book_dir}（请先运行 run.py render）")
        return 2

    failures = []
    metrics = measure(book_dir, args.verbose)
    if metrics is None:
        return 2
    failures.extend(check_measured(metrics))
    anchor_failures, anchor_total = check_anchors(book_dir)
    failures.extend(anchor_failures)

    if args.verbose:
        for width_text, pages in metrics["viewports"].items():
            for page_id, data in pages.items():
                print("  %s@%s 正文高=%s 段落宽=%s 带/盒=%s/%s 连续盒=%s 目录项=%s 溢出=%s" % (
                    page_id, width_text, data["contentHeight"], data["paragraphWidth"],
                    data["textBandCount"], data["boxCount"], data["consecutiveBoxes"],
                    max((item["height"] for item in data["tocItems"]), default=0), len(data["overflow"])))

    print(f"  锚点引用 {anchor_total} 条，全部可解析" if not anchor_failures
          else f"  锚点引用 {anchor_total} 条，失败 {len(anchor_failures)} 条")
    if failures:
        print("FAIL typography")
        for line in failures:
            print("  " + line)
        return 1
    print(f"PASS typography 布局与密度闸门（两档视口 × {len(PAGES)} 页 + {anchor_total} 条锚点）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
