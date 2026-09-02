#!/usr/bin/env python3
"""从 cpp-topic 模板生成新的 C++ 主题章节骨架。

用法：
  python scaffold_chapter.py --topic <ascii-name> [--part <part>] [--title "中文标题"]
创建 content/<part>/<topic>.qmd（title 已填入；--part 默认与 topic 同名），
模板位于 .cursor/skills/cpp-content/templates/cpp-topic.qmd。
part 索引页 index.qmd 不由本脚本生成。
之后需手动在 _quarto.yml 的 book.chapters 注册，并运行 verify_examples.py。

退出码：0 = 创建成功；1 = 参数/路径错误。
"""

import argparse
import os
import re
import sys

TOPIC_RE = re.compile(r"^[A-Za-z0-9_-]+$")
TITLE_RE = re.compile(r'(?m)^title: ".*"')


def fail(msg):
    print(f"错误：{msg}")
    return 1


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="章节名（纯 ASCII：字母/数字/-/_）")
    parser.add_argument("--part", default="", help="父目录名（part 主题目录；默认与 topic 同名）")
    parser.add_argument("--title", default="", help="显示标题（默认用 topic 名）")
    parser.add_argument(
        "--skill-root", default=os.path.join(".cursor", "skills", "cpp-content"),
        help="cpp-content skill 根目录（相对仓库根）",
    )
    parser.add_argument("--content-root", default="content", help="章节根目录")
    args = parser.parse_args()

    if not TOPIC_RE.match(args.topic):
        return fail(f"Topic 必须为纯 ASCII（字母/数字/-/_），收到：{args.topic}")
    part = args.part or args.topic
    if not TOPIC_RE.match(part):
        return fail(f"Part 必须为纯 ASCII（字母/数字/-/_），收到：{part}")

    template = os.path.join(args.skill_root, "templates", "cpp-topic.qmd")
    if not os.path.isfile(template):
        return fail(f"模板不存在：{template}")

    target_dir = os.path.join(args.content_root, part)
    target_file = os.path.join(target_dir, f"{args.topic}.qmd")
    if os.path.exists(target_file):
        return fail(f"目标已存在（中止）：{target_file}")

    with open(template, encoding="utf-8") as fh:
        content = fh.read()
    if not re.search(r"(?m)^title: ", content):
        return fail("模板缺少 title: 行，中止。")

    display_title = args.title or args.topic
    content = TITLE_RE.sub(f'title: "{display_title}"', content, count=1)

    os.makedirs(target_dir, exist_ok=True)
    with open(target_file, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)

    print(f"Created: {target_file}")
    print(f"  - title set to: {display_title}")
    print(f"Next: 在 _quarto.yml 的 book.chapters 注册 {target_file}，"
          f"然后运行 verify_examples.py。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
