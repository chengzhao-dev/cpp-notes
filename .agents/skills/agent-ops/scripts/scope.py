#!/usr/bin/env python3
"""解析任务作用域，输出本次任务「该读什么 / 不该读什么」的最小清单。

为什么需要它：上下文的量不是靠自觉控制，而是由构造封顶。本脚本按仓库既有的
目录命名约定（content/<part>/<chapter>.qmd <-> code/<part>/<chapter>[/]）反查出
当前任务的最小文件集，并把构建产物、渲染产物、其它章节一律列入 DENY。
调用方只需读 UNIT+READ 所列文件，其余不碰——省掉「整包多读」与「反复枚举目录」。

零新增元数据：路由表就是 .agents/skills/cpp-content/references/tasks/<part>.md 任务矩阵。
「公共必读」行给出该 part 每章共用的 reference，矩阵行的「专项必读」列给出该章独有的部分，
「状态」列给出是否已开工，因此矩阵改名或合并章节都不需要改本脚本。

用法：
  python scope.py <part>/<chapter>      # 一个章节单元（矩阵登记即可解析，正文可尚未存在）
  python scope.py <仓库内任意路径>       # 由路径反查其所属单元
  python scope.py theme|dev|repo        # 非章节类域任务
  python scope.py --list                # 列出矩阵登记的全部章节单元与状态
退出码：0 = 解析成功，1 = 目标无法解析（提示按约定命名，不做猜测）。
"""

import argparse
import re
import sys
from pathlib import Path

# 构建产物目录：任何情况下都不进上下文（内含 CMakeCXXCompilerId.cpp 等生成物，
# 其中含 int main，误读会污染示例校验与写作判断）
BUILD_DIRS = ("build", ".cache", ".tmp", "temp", "__pycache__")
ALWAYS_DENY = [
    "_book/**（渲染产物：校验走 .agents/skills/agent-ops/scripts/check_dom_contracts.py，不直接读）",
    "code/**/build/**（CMake 产物：永不入上下文）",
    ".quarto/**（Quarto 缓存）",
    "**/.cache/**（工具缓存）",
    "**/.tmp/**（临时文件）",
    "temp/**（统一临时产物目录）",
    # 宿主六项原则文件：只服务个性化设置，永不作为任务阅读项
    "宿主个性化说明（六项原则，来自用户全局配置）：不列入 UNIT/READ",
]
# 单个单元的代码文件上限：超出则只报计数，避免清单本身膨胀
MAX_UNIT_FILES = 12
TASKS_DIR = ".agents/skills/cpp-content/references/tasks"
MERGED = "merged"
# 反查单元时用来剥离文件后缀（章节名与 chapter 同名，含连字符与 .cpp/.qmd/.txt）
STEM_RE = re.compile(r"\.(qmd|cpp|cc|cxx|h|hpp|txt|sh|json|py)$")

TICK_RE = re.compile(r"`([^`]+)`")
REPO_PATH_PREFIX = (".agents/", "knowledge/", "content/", "code/")


def repo_root():
    return Path(__file__).resolve().parents[4]


def rel(path, root):
    return path.relative_to(root).as_posix()


def is_code_dir(entry):
    """判断目录内是否存在构建产物子目录，用于提示。"""
    return any((entry / b).is_dir() for b in BUILD_DIRS)


def unit_files(directory, root):
    """列出一个代码目录里的源文件，剔除构建产物。"""
    out = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if any(part in BUILD_DIRS for part in path.relative_to(directory).parts[:-1]):
            continue
        out.append(rel(path, root))
    return out


def repo_paths(text):
    """从一行文本里取出反引号包裹的仓库路径，去重保序。"""
    seen, uniq = set(), []
    for cand in TICK_RE.findall(text):
        cand = cand.strip().strip("()")
        if cand.startswith(REPO_PATH_PREFIX) and cand not in seen:
            seen.add(cand)
            uniq.append(cand)
    return uniq


def matrix_path(root, part):
    """part 对应的任务矩阵文件。不存在返回 None。"""
    path = root / TASKS_DIR / f"{part}.md"
    return path if path.is_file() else None


def parse_matrix(path):
    """解析任务矩阵表格，返回 {chapter: {tid, status, dep, qmd, code, spec, note}}。"""
    rows = {}
    if not path or not path.is_file():
        return rows
    common = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("- **必读**"):
            common = repo_paths(line)
            break
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("| `TASK-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8:
            continue
        tid = cells[0].strip("`")
        rows[cells[1].strip("`")] = {
            "tid": tid,
            "status": cells[2],
            "dep": cells[3].strip("`"),
            "qmd": first_path(cells[4]),
            "code": first_path(cells[5]),
            "spec": [p for p in repo_paths(cells[6]) if p not in common],
            "note": "" if cells[7] in ("—", "-") else cells[7],
            "common": common,
        }
    return rows


def first_path(cell):
    """取单元格里的第一个仓库路径。「—（不新建）」之类返回空串。"""
    paths = repo_paths(cell)
    return paths[0] if paths else ""


def find_chapter(target, root):
    """把 <part>/<chapter> 解析成章节单元（以任务矩阵登记为准）。"""
    if "/" not in target:
        return None
    part, chapter = target.split("/", 1)
    matrix_file = matrix_path(root, part)
    row = parse_matrix(matrix_file).get(chapter)
    if row is None:
        return None
    qmd = root / "content" / part / f"{chapter}.qmd"
    return {"kind": "chapter", "part": part, "chapter": chapter,
            "qmd": qmd if qmd.is_file() else None, "matrix": matrix_file, "row": row}


def resolve_path(target, root):
    """由任意仓库内路径反查所属章节单元。

    `content/<part>/<chapter>.qmd` 与 `code/<part>/<chapter>.cpp` 取文件主名，
    `code/<part>/<chapter>/...` 取第三段目录名。两者都要求章节已在矩阵登记。
    """
    path = (root / target).resolve()
    try:
        parts = rel(path, root).split("/")
    except ValueError:
        return None
    if len(parts) < 3 or parts[0] not in ("content", "code"):
        return None
    part = parts[1]
    chapter = parts[2] if len(parts) > 3 else STEM_RE.sub("", parts[2])
    if not chapter or chapter == "index" or chapter == ".gitkeep":
        return None
    return find_chapter(f"{part}/{chapter}", root)


DOMAIN_READ = {
    "theme": [".agents/skills/quarto-theme/SKILL.md",
              ".agents/skills/quarto-theme/references/theme-system.md"],
    "dev": [".agents/skills/agent-ops/assets/config/editorconfig",
            ".agents/skills/python-tools/scripts/scaffold/"],
    "repo": ["AGENTS.md", ".agents/skills/catalog.md",
             ".agents/skills/agent-ops/references/repository-structure.md"],
}


def resolve_repo_domain(target, root):
    """把 skill、Knowledge、MCP 或任意仓库路径解析成最小读取域。"""
    path = (root / target).resolve()
    try:
        rel_path = rel(path, root)
    except ValueError:
        return None
    parts = rel_path.split("/")
    if parts[:2] == [".agents", "skills"]:
        if len(parts) == 2:
            return {
                "kind": "repo",
                "label": "skills",
                "reads": [".agents/skills/catalog.md"],
            }
        skill = parts[2]
        reads = [".agents/skills/catalog.md", f".agents/skills/{skill}/SKILL.md"]
        if len(parts) > 3 and path.is_file():
            reads.append(rel_path)
        elif len(parts) > 3 and path.is_dir():
            reads.append(rel_path + "/")
        return {"kind": "repo", "label": f"skill {skill}", "reads": reads}
    if parts[:2] == [".agents", "mcp"]:
        return {
            "kind": "repo",
            "label": "mcp",
            "reads": [".agents/mcp/README.md", rel_path],
        }
    if parts and parts[0] == "knowledge":
        reads = ["knowledge/README.md"]
        if len(parts) > 1 and path.is_file():
            reads.append(rel_path)
        elif len(parts) > 1 and path.is_dir():
            reads.append(rel_path + "/")
        return {"kind": "repo", "label": "knowledge", "reads": reads}
    if path.exists():
        return {"kind": "repo", "label": "path", "reads": [rel_path]}
    return None


def emit(unit, root, out, verbose=False):
    """按固定格式打印 UNIT/READ/DENY 三段。"""
    lines = out

    if unit["kind"] == "chapter":
        part, chapter, row = unit["part"], unit["chapter"], unit["row"]
        lines.append(f"SCOPE chapter {part}/{chapter}")
        lines.append(f"TASK  {row['tid']} 状态={row['status']} 前置={row['dep'] or '—'}")
        if row["status"].startswith(MERGED):
            lines.append(f"HOLD  本章已并入 {row['dep'] or '前置章节'}，不新建正文；{row['note']}")
            lines.append("RULE  只读 UNIT+READ；确需越界先一句声明理由（诊断逃生舱）")
            return
        if unit["qmd"]:
            lines.append(f"UNIT  {rel(unit['qmd'], root)}")
        else:
            lines.append(f"UNIT  content/{part}/{chapter}.qmd（待新建）")
        single = root / "code" / part / f"{chapter}.cpp"
        code_dir = root / "code" / part / chapter
        if single.is_file():
            lines.append(f"UNIT  {rel(single, root)}")
        elif code_dir.is_dir():
            files = unit_files(code_dir, root)
            shown = files if verbose else files[:MAX_UNIT_FILES]
            for item in shown:
                lines.append(f"UNIT  {item}")
            if not verbose and len(files) > MAX_UNIT_FILES:
                lines.append(f"UNIT  …共 {len(files)} 个源文件（已截断，--verbose 看全量）")
            if is_code_dir(code_dir):
                lines.append(f"HOLD  code/{part}/{chapter}/build/ 存在构建产物：已排除，勿读")
        lines.append(f"UNIT  {rel(unit['matrix'], root)}（任务矩阵：读写边界、状态与验收）")
        for ref in row["common"]:
            mark = "" if (root / ref).is_file() else "  ← 文件不存在，请核对"
            lines.append(f"READ  {ref}{mark}")
        for ref in row["spec"]:
            mark = "" if (root / ref).is_file() else "  ← 文件不存在，请核对"
            lines.append(f"READ  {ref}{mark}（本章专项）")
        lines.append("DENY  其它 content/** 与 code/** 单元（跨章只按 @sec- 引用，不读正文）")
    else:
        label = unit.get("label", unit["kind"])
        lines.append(f"SCOPE {unit['kind']} {label}".rstrip())
        refs = unit.get("reads") or DOMAIN_READ[unit["kind"]]
        for ref in refs:
            lines.append(f"READ  {ref}")
        if unit["kind"] == "theme":
            lines.append("RULE  只读取与当前任务直接相关的那一个主题资源或 CSS，禁止通读整个 css/。")
        lines.append("DENY  content/** 与 code/**（本域任务不改正文与示例）")

    for deny in ALWAYS_DENY:
        lines.append(f"DENY  {deny}")
    lines.append("RULE  只读 UNIT+READ；确需越界先一句声明理由（诊断逃生舱）")
    return lines


def all_units(root):
    """列出任务矩阵登记的全部章节单元：[(part/chapter, tid, status)]。"""
    units = []
    for matrix in sorted((root / TASKS_DIR).glob("*.md")):
        for chapter, row in sorted(parse_matrix(matrix).items()):
            units.append((f"{matrix.stem}/{chapter}", row["tid"], row["status"]))
    return units


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="解析任务作用域（UNIT/READ/DENY 清单）")
    parser.add_argument("target", nargs="?", help="章节 <part>/<chapter>、skill/knowledge/MCP/仓库内路径，或 theme/dev/repo")
    parser.add_argument("--list", action="store_true", help="列出任务矩阵登记的全部章节单元")
    parser.add_argument("--verbose", action="store_true", help="展开被截断的 UNIT 文件")
    args = parser.parse_args()

    root = repo_root()

    if args.list:
        units = all_units(root)
        for unit, tid, status in units:
            print(f"{unit}\t{tid}\t{status}")
        todo = sum(1 for _u, _t, s in units if s == "todo")
        print(f"（共 {len(units)} 个章节单元：todo {todo}，其余 done/merged）")
        return 0

    if not args.target:
        print("错误：缺少目标。用法见 python scope.py --help")
        return 1

    target = args.target.strip().strip("/\\").replace("\\", "/")

    if target in DOMAIN_READ:
        unit = {"kind": target}
    else:
        unit = find_chapter(target, root) or resolve_path(target, root) or resolve_repo_domain(target, root)

    if not unit:
        print(f"无法解析目标：{target}")
        print("支持形式：<part>/<chapter>、skill/knowledge/MCP/仓库内路径，或 theme/dev/repo。")
        print("章节须先在 .agents/skills/cpp-content/references/tasks/<part>.md 任务矩阵登记；")
        print("未登记时请按约定补行，本脚本不做猜测。可用 --list 查看现有单元。")
        return 1

    out = []
    emit(unit, root, out, args.verbose)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
