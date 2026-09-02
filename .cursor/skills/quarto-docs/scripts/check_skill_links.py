#!/usr/bin/env python3
"""检查所有 skills 的内部链接是否可解析。

覆盖范围：.cursor/skills/*/SKILL.md + references/**/*.md + templates/*.qmd。
校验的链接形态：
  - references/...、templates/...（skill 根相对路径）
  - scripts/...（skill 根相对路径；未命中时回退按仓库根 scripts/ 解析，两处任一存在即通过）
  - ./、../ 相对路径（含跨 skill 的 ../..）
  - .cursor/... 全仓库路径
仅校验以 .md / .qmd / .py 结尾的引用，跳过示例命令路径（如 ./build/main）。

用法：python check_skill_links.py
退出码：0 = 全部链接可达；1 = 存在断链。
"""

import os
import re
import sys

LINK_RE = re.compile(
    r"\.cursor/[A-Za-z0-9_./-]+"
    r"|(?:references|templates|scripts)/[A-Za-z0-9_./-]+"
    r"|\.{1,2}/[A-Za-z0-9_./-]+"
)
VALID_EXT_RE = re.compile(r"\.(md|qmd|py)$")


def collect_files(skills_root):
    files = []
    for name in sorted(os.listdir(skills_root)):
        skill_dir = os.path.join(skills_root, name)
        if not os.path.isdir(skill_dir):
            continue
        candidates = [os.path.join(skill_dir, "SKILL.md")]
        refs = os.path.join(skill_dir, "references")
        if os.path.isdir(refs):
            for dirpath, _, filenames in os.walk(refs):
                candidates.extend(
                    os.path.join(dirpath, fn) for fn in filenames if fn.endswith(".md")
                )
        templates = os.path.join(skill_dir, "templates")
        if os.path.isdir(templates):
            candidates.extend(
                os.path.join(templates, fn) for fn in sorted(os.listdir(templates))
                if fn.endswith(".qmd")
            )
        files.extend(c for c in candidates if os.path.isfile(c))
    return files


def resolve_link(repo_root, skill_root, file_dir, link):
    """把三种形态的链接解析为仓库内绝对路径。"""
    if link.startswith(".cursor/"):
        base, rel = repo_root, link
    elif link.startswith("./") or link.startswith("../"):
        base, rel = file_dir, link
    else:
        base, rel = skill_root, link
    return os.path.normpath(os.path.join(base, rel.replace("/", os.sep)))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    repo_root = os.getcwd()
    skills_root = os.path.join(repo_root, ".cursor", "skills")
    if not os.path.isdir(skills_root):
        print(f"skills 目录不存在：{skills_root}")
        return 1

    bad = []
    for f in collect_files(skills_root):
        rel = os.path.relpath(f, skills_root).replace(os.sep, "/")
        skill_root = os.path.join(skills_root, rel.split("/")[0])
        file_dir = os.path.dirname(f)
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        for m in LINK_RE.finditer(text):
            link = m.group(0)
            if not VALID_EXT_RE.search(link):
                continue  # 跳过示例命令路径等非文档引用
            target = resolve_link(repo_root, skill_root, file_dir, link)
            if not os.path.exists(target) and link.startswith("scripts/"):
                # 仓库根 scripts/（AGENTS.md 定义的仓库级脚本目录）同样合法
                target = os.path.normpath(os.path.join(repo_root, link))
            if not os.path.exists(target):
                bad.append((rel, link, os.path.relpath(target, repo_root)))

    if not bad:
        print("OK: all internal references/templates/scripts and relative links resolve.")
        return 0

    print(f"Found {len(bad)} broken link(s):")
    for rel, link, target in bad:
        print(f"  {rel} -> {link} (resolved: {target})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
