#!/usr/bin/env python3
"""解析任务作用域，输出本次任务「该读什么 / 不该读什么」的最小清单。

为什么需要它：上下文的量不是靠自觉控制，而是由构造封顶。本脚本按仓库既有的
目录命名约定（content/<part>/<chapter>.qmd ↔ code/<part>/<chapter>[/]）反查出
当前任务的最小文件集，并把构建产物、渲染产物、其它章节一律列入 DENY。
调用方只需读 UNIT+READ 所列文件，其余不碰——省掉「整包多读」与「反复枚举目录」。

零新增元数据：READ 清单直接解析 docs/tasks/**/<chapter>.md 里的「必读」行，
不引入额外的清单文件；任务单本身就是路由表。

用法：
  python scope.py <part>/<chapter>      # 一个章节单元
  python scope.py <仓库内任意路径>       # 由路径反查其所属单元
  python scope.py theme|dev|repo        # 非章节类域任务
  python scope.py --list                # 列出全部可解析的章节单元
退出码：0 = 解析成功；1 = 目标无法解析（提示按约定命名，不做猜测）。
"""

import argparse
import re
import sys
from pathlib import Path

# 构建产物目录：任何情况下都不进上下文（内含 CMakeCXXCompilerId.cpp 等生成物，
# 其中含 int main，误读会污染示例校验与写作判断）
BUILD_DIRS = ("build",)
ALWAYS_DENY = [
    "_book/**（渲染产物：校验走 scripts/agent/check_dom_contracts.py，不直接读）",
    "code/**/build/**（CMake 产物：永不入上下文）",
    ".quarto/**（Quarto 缓存）",
]
# 单个单元的代码文件上限：超出则只报计数，避免清单本身膨胀
MAX_UNIT_FILES = 12

TICK_RE = re.compile(r"`([^`]+)`")


def repo_root():
    return Path(__file__).resolve().parents[2]


def rel(path, root):
    return path.relative_to(root).as_posix()


def is_code_dir(entry):
    """判断目录内是否存在构建产物子目录，用于提示。"""
    return any((entry / b).is_dir() for b in BUILD_DIRS)


def unit_files(directory, root):
    """列出一个代码目录里的源文件，剔除构建产物。"""
    out = []
    for p in sorted(directory.rglob("*")):
        if not p.is_file():
            continue
        if any(part in BUILD_DIRS for part in p.relative_to(directory).parts[:-1]):
            continue
        out.append(rel(p, root))
    return out


def parse_required_read(task_file):
    """从任务单的「必读」行提取文件路径（反引号包裹 + 行内链接目标）。"""
    if not task_file.is_file():
        return []
    paths = []
    for line in task_file.read_text(encoding="utf-8").splitlines():
        if "必读" not in line:
            continue
        for cand in TICK_RE.findall(line):
            cand = cand.strip().strip("()")
            if cand.startswith(".cursor/") or cand.startswith("docs/") or cand.startswith("content/"):
                paths.append(cand)
            elif cand.startswith("../../"):
                # 任务单相对路径：归一到仓库根再取 POSIX 形式
                norm = (task_file.parent / cand).resolve()
                try:
                    paths.append(rel(norm, repo_root()))
                except ValueError:
                    pass
        break
    # 去重且保序
    seen, uniq = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def find_chapter(target, root):
    """把 <part>/<chapter> 解析成章节单元。"""
    if "/" not in target:
        return None
    part, chapter = target.split("/", 1)
    qmd = root / "content" / part / f"{chapter}.qmd"
    task = root / "docs" / "tasks" / "content" / part / f"{chapter}.md"
    if not qmd.is_file():
        qmd = None
    return {"kind": "chapter", "part": part, "chapter": chapter,
            "qmd": qmd, "task": task if task.is_file() else None}


def resolve_path(target, root):
    """由任意仓库内路径反查所属章节单元。"""
    p = (root / target).resolve()
    try:
        parts = rel(p if p.is_dir() else p.parent, root).split("/")
    except ValueError:
        return None
    if len(parts) >= 2 and parts[0] in ("content", "code") and parts[1] != ".gitkeep":
        part = parts[1]
        # content/<part>/<chapter>.qmd 或 code/<part>/<chapter>[...]
        name = parts[2] if len(parts) > 2 else ""
        chapter = re.sub(r"\.(qmd|cpp|txt|sh|json)$", "", name)
        if chapter:
            found = find_chapter(f"{part}/{chapter}", root)
            if found and (found["qmd"] or found["task"]):
                return found
            # 目录式代码：code/<part>/<chapter>/
            if (root / "content" / part / f"{chapter}.qmd").is_file():
                return find_chapter(f"{part}/{chapter}", root)
    return None


DOMAIN_READ = {
    "theme": ["theme/css/", ".cursor/skills/quarto-theme/SKILL.md",
              ".cursor/skills/quarto-theme/references/design-tokens.md"],
    "dev": [".clangd", ".clang-format", ".editorconfig", ".vscode/"],
    "repo": ["docs/structure.md", "AGENTS.md"],
}


def emit(unit, root, out):
    """按固定格式打印 UNIT/READ/DENY 三段。"""
    lines = out  # 局部别名，便于阅读

    if unit["kind"] == "chapter":
        part, chapter = unit["part"], unit["chapter"]
        lines.append(f"SCOPE chapter {part}/{chapter}")
        if unit["qmd"]:
            lines.append(f"UNIT  {rel(unit['qmd'], root)}")
        single = root / "code" / part / f"{chapter}.cpp"
        code_dir = root / "code" / part / chapter
        if single.is_file():
            lines.append(f"UNIT  {rel(single, root)}")
        elif code_dir.is_dir():
            files = unit_files(code_dir, root)
            for f in files[:MAX_UNIT_FILES]:
                lines.append(f"UNIT  {f}")
            if len(files) > MAX_UNIT_FILES:
                lines.append(f"UNIT  …共 {len(files)} 个源文件（已截断，--verbose 看全量）")
            if is_code_dir(code_dir):
                lines.append(f"HOLD  code/{part}/{chapter}/build/ 存在构建产物：已排除，勿读")
        if unit["task"]:
            lines.append(f"UNIT  {rel(unit['task'], root)}（任务单：读写边界与验收）")
        for ref in parse_required_read(unit["task"] or Path()) if unit["task"] else []:
            exists = (root / ref).is_file()
            lines.append(f"READ  {ref}{'' if exists else '  ← 文件不存在，请核对'}")
        lines.append("DENY  其它 content/** 与 code/** 单元（跨章只按 @sec- 引用，不读正文）")
    else:
        lines.append(f"SCOPE {unit['kind']}")
        for ref in DOMAIN_READ[unit["kind"]]:
            lines.append(f"READ  {ref}")
        lines.append("DENY  content/** 与 code/**（本域任务不改正文与示例）")

    for d in ALWAYS_DENY:
        lines.append(f"DENY  {d}")
    lines.append("RULE  只读 UNIT+READ；确需越界先一句声明理由（诊断逃生舱）")
    return lines


def all_units(root):
    out = []
    for qmd in sorted((root / "content").glob("*/*.qmd")):
        part = qmd.parent.name
        chapter = qmd.stem
        if chapter == "index":
            continue
        out.append(f"{part}/{chapter}")
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="解析任务作用域（UNIT/READ/DENY 清单）")
    parser.add_argument("target", nargs="?", help="章节 <part>/<chapter>、仓库内路径，或 theme/dev/repo")
    parser.add_argument("--list", action="store_true", help="列出全部可解析的章节单元")
    args = parser.parse_args()

    root = repo_root()

    if args.list:
        for u in all_units(root):
            print(u)
        print(f"（共 {len(all_units(root))} 个章节单元）")
        return 0

    if not args.target:
        print("错误：缺少目标。用法见 python scope.py --help")
        return 1

    target = args.target.strip().strip("/\\").replace("\\", "/")

    if target in DOMAIN_READ:
        unit = {"kind": target}
    else:
        unit = find_chapter(target, root)
        if unit and (unit["qmd"] or unit["task"]):
            pass
        else:
            unit = resolve_path(target, root)

    if not unit:
        print(f"无法解析目标：{target}")
        print("支持形式：<part>/<chapter>、仓库内路径、或 theme/dev/repo。")
        print("章节需与目录命名约定对齐（content/<part>/<chapter>.qmd ↔ code/<part>/<chapter>）；")
        print("不匹配时请按约定重命名，本脚本不做猜测。可用 --list 查看现有单元。")
        return 1

    out = []
    emit(unit, root, out)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())