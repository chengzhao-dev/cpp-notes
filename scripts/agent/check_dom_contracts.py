#!/usr/bin/env python3
"""校验渲染产物（_book）里的「结构契约」，防止已修过的 HTML/CSS 联动 bug 复发。

为什么需要它：Quarto 升级会改动代码块的 DOM（例如复制按钮从 div.sourceCode 的
后代变成兄弟），这类问题在任何单一源文件中都看不出来——只有把「产物结构」和
「CSS 选择器」放在一起校验才能发现。本脚本把历史上真实踩过的坑固化成断言。

省 token 的机制：脚本自己去读产物里那些几十 KB 的 HTML/CSS，对外只输出
每条契约一行的结论（PASS/MISS）。正常情况下人肉读 _book 的必要性被消除；
只有某条契约报 FAIL 时，才需要开诊断模式去看具体文件。

契约清单：
  C1 复制按钮可见性：产物中 button.code-copy-button 必须与 div.sourceCode
     同处 .code-copy-outer-scaffold 之下且互为兄弟；且 CSS 里必须存在
     .code-copy-outer-scaffold:hover .code-copy-button 规则。
     （若选择器仍写成 div.sourceCode:hover 的后代形式，hover 永不生效。）
  C2 触屏兜底：CSS 必须包含 @media (hover: none) 下的 .code-copy-button 可见规则，
     否则移动端永远无法复制代码。
  C3 打印不隐藏代码：@media print 内不得对 .code-copy-outer-scaffold 设 display:none。
     （该层现在包裹代码本身，隐藏它 = 打印/PDF 时代码整块消失。）
  C4 站点图标：每个 HTML 的 <head> 必须含 rel="icon" 且指向 favicon.svg，
     且该图标文件确实被发布到产物目录。

用法：python check_dom_contracts.py [--book-dir _book] [--verbose]
退出码：0 = 全部契约通过；1 = 有契约失败；2 = 产物目录不存在（需先 quarto render）。
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SCAFFOLD = "code-copy-outer-scaffold"
COPY_BTN = "code-copy-button"
SRCODE = "sourceCode"

# 无闭合标签的元素：不入栈，否则解析栈会被打乱
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class Node:
    """极简 DOM 节点：只保留契约所需的 tag / class / 父子关系。"""

    __slots__ = ("tag", "classes", "children", "parent")

    def __init__(self, tag, classes, parent):
        self.tag = tag
        self.classes = set(classes)
        self.children = []
        self.parent = parent


class TreeBuilder(HTMLParser):
    """把 HTML 解析成只含 class 信息的轻量树，避免引入第三方解析库。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", set(), None)
        self.stack = [self.root]
        self.link_rels = []  # [(rel, href)] 供 favicon 契约使用

    def handle_starttag(self, tag, attrs):
        attrd = dict(attrs)
        classes = (attrd.get("class") or "").split()
        node = Node(tag, classes, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag == "link":
            self.link_rels.append(((attrd.get("rel") or "").lower(), attrd.get("href") or ""))
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_endtag(self, tag):
        # 容忍源文档里缺失的闭合标签（Quarto 输出常有）：向上回溯到匹配的开标签
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return


def walk(node):
    for child in node.children:
        yield child
        yield from walk(child)


def is_descendant(node, ancestor):
    parent = node.parent
    while parent is not None:
        if parent is ancestor:
            return True
        parent = parent.parent
    return False


def normalize(css):
    """压掉注释与多余空白，让选择器匹配不受换行/缩进影响。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return re.sub(r"\s+", " ", css)


def collect_css(book_dir):
    texts = []
    for path in sorted(book_dir.rglob("*.css")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if SCAFFOLD in raw or COPY_BTN in raw or "@media" in raw:
            texts.append((path, normalize(raw)))
    return texts


def media_blocks(css, keyword):
    """提取 @media <keyword> 整块内容（含嵌套），按花括号配平扫描。"""
    blocks = []
    for m in re.finditer(r"@media[^{]*\b" + keyword + r"\b[^{]*\{", css):
        depth = 1
        i = m.end()
        while i < len(css) and depth:
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
            i += 1
        if depth == 0:
            blocks.append(css[m.end():i - 1])
    return blocks


def rules_of(block_css):
    """把一段 CSS 拆成 (selector, body) 列表（跳过嵌套的 @规则首部）。"""
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", block_css):
        out.append((m.group(1).strip(), m.group(2)))
    return out


def hidden_selectors(block_css, needle):
    """返回该 CSS 块中对 needle 设了 display:none 的选择器列表。"""
    hits = []
    for selector, body in rules_of(block_css):
        if needle in selector and re.search(r"display\s*:\s*none", body):
            hits.append(selector)
    return hits


def check_contracts(book_dir, htmls, css_pairs):
    """跑完全部契约，返回 [(id, 名称, ok, 摘要, [细节行])]。"""
    results = []

    # ---------- C1 复制按钮可见性 ----------
    sibling_ok = False
    scaffold_pages = 0
    for path, tree, _rels in htmls:
        scaffolds = [n for n in walk(tree) if SCAFFOLD in n.classes]
        if not scaffolds:
            continue
        scaffold_pages += 1
        for sc in scaffolds:
            code = [c for c in sc.children if c.tag == "div" and SRCODE in c.classes]
            btns = [c for c in sc.children if c.tag == "button" and COPY_BTN in c.classes]
            if code and btns and not any(is_descendant(b, code[0]) for b in btns):
                sibling_ok = True
    hover_rule = any(
        ".%s:hover .%s" % (SCAFFOLD, COPY_BTN) in css for _, css in css_pairs
    )
    stale_rule = any(
        "div.%s:hover .%s" % (SRCODE, COPY_BTN) in css for _, css in css_pairs
    )
    c1 = sibling_ok and hover_rule and not stale_rule
    results.append((
        "C1", "复制按钮 hover 可见（兄弟 DOM + scaffold 选择器）", c1,
        "pages=%d sibling=%s hover-rule=%s%s"
        % (scaffold_pages, sibling_ok, hover_rule, " stale-rule!" if stale_rule else ""),
        [
            "产物中 button.%s 必须与 div.%s 同为 .%s 的直接子元素" % (COPY_BTN, SRCODE, SCAFFOLD),
            "CSS 必须含 .%s:hover .%s（不能停留在 div.%s:hover 的后代写法）"
            % (SCAFFOLD, COPY_BTN, SRCODE),
        ],
    ))

    # ---------- C2 触屏兜底 ----------
    touch_ok = False
    for _, css in css_pairs:
        for block in media_blocks(css, "hover: none"):
            if COPY_BTN in block and re.search(r"opacity\s*:\s*1", block):
                touch_ok = True
    results.append((
        "C2", "触屏无 hover 时复制按钮仍可见", touch_ok,
        "@media (hover: none) 规则=%s" % touch_ok,
        ["CSS 需含 @media (hover: none) { .%s { opacity: 1 } }" % COPY_BTN],
    ))

    # ---------- C3 打印不隐藏代码 ----------
    offenders = []
    for path, css in css_pairs:
        for block in media_blocks(css, "print"):
            for sel in hidden_selectors(block, SCAFFOLD):
                offenders.append("%s: %s" % (path.name, sel))
    c3 = not offenders
    results.append((
        "C3", "打印/PDF 时代码块不被隐藏", c3,
        "违规规则数=%d" % len(offenders),
        ["@media print 内不得对 .%s 设 display:none（它现在包裹代码本身），只可隐藏 .%s"
         % (SCAFFOLD, COPY_BTN)] + offenders,
    ))

    # ---------- C4 favicon ----------
    icon_pages = 0
    missing = []
    for path, _tree, link_rels in htmls:
        rels = [(r, h) for r, h in link_rels if "icon" in r]
        if any("favicon.svg" in h for r, h in rels):
            icon_pages += 1
        else:
            missing.append(str(path.relative_to(book_dir)))
    icon_file = any(p.name == "favicon.svg" for p in book_dir.rglob("favicon.svg"))
    c4 = icon_pages == len(htmls) and icon_file and bool(htmls)
    summary = "%d/%d 页含 icon 链接，图标已发布=%s" % (icon_pages, len(htmls), icon_file)
    if missing:
        summary += "；缺链接: " + ", ".join(missing[:3])
        if len(missing) > 3:
            summary += " …"
    results.append((
        "C4", "站点图标已注入并发布", c4, summary,
        ["每页 <head> 需 <link rel=\"icon\" … favicon.svg>；源文件见 theme/assets/favicon.svg，"
         "由 scripts/maint/gen_favicon.py 生成"],
    ))

    return results


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="校验渲染产物中的结构契约")
    parser.add_argument("--book-dir", default="_book", help="渲染产物目录（默认 _book）")
    parser.add_argument("--verbose", action="store_true", help="失败时展开修复指引")
    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    if not book_dir.is_dir():
        print("MISS 产物目录不存在：%s（请先运行 quarto render）" % book_dir)
        return 2

    htmls = []
    for path in sorted(book_dir.rglob("*.html")):
        builder = TreeBuilder()
        try:
            builder.feed(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        htmls.append((path, builder.root, builder.link_rels))

    if not htmls:
        print("MISS 未找到任何 HTML：%s" % book_dir)
        return 1

    css_pairs = collect_css(book_dir)
    results = check_contracts(book_dir, htmls, css_pairs)

    # 默认每条契约只占一行，失败项排前面，方便快速定位
    failed = 0
    for cid, name, ok, summary, hints in sorted(results, key=lambda r: r[2]):
        if not ok:
            failed += 1
        print("%s %s %s  (%s)" % ("OK  " if ok else "FAIL", cid, name, summary))
        if not ok and args.verbose:
            for line in hints:
                print("       · %s" % line)

    print()
    if failed == 0:
        print("DOM contracts: %d/%d PASS" % (len(results), len(results)))
        return 0
    print("DOM contracts: %d 项失败，需开诊断模式定位（见 --verbose）" % failed)
    return 1


if __name__ == "__main__":
    sys.exit(main())