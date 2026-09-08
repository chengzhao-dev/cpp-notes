#!/usr/bin/env python3
"""知识库共享工具：路径解析、Markdown 标题树解析、统一的令牌估算口径。

分块、索引、检索、体检四步都要这三件事，各写一份必然漂移，所以集中在这里：
  1. 定位仓库根与 knowledge/ 布局
  2. 围栏感知地切出标题层级（## 是 Parent 边界，### 是 Child 边界）
  3. 用同一口径估算令牌

估算口径是启发式（CJK 每字 1、拉丁串每 4 字符 1），不是真实分词器。索引与检索
共用同一个函数，因此排序、预算裁剪和体检对同一个 Chunk 的令牌判断始终一致。

写这个仓库里的文件时注意：反斜杠在 PowerShell 与 JSON 参数传输中会被吞掉或翻倍，
所以本模块的正文一律不含反斜杠，正则里的空白与换行用字符类和 chr() 表达。
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = ROOT / "knowledge"
DOMAINS_ROOT = KB_ROOT / "domains"
BRANCHES_ROOT = KB_ROOT / "branches"
INDEX_DIR = ROOT / "index_data"
REGISTRY_PATH = INDEX_DIR / "chunk_registry.json"
DB_PATH = INDEX_DIR / "kb_index.sqlite"
DEFAULT_BRANCH = "main"

NL = chr(10)
SPACES = " " + chr(9)
FENCE_RE = re.compile("^(" + chr(96) + "{3,}|~{3,})")
HEADING_RE = re.compile("^(#{1,6})[" + SPACES + "]+(.+)$")
WORD_RE = re.compile("[A-Za-z0-9_]+")
REQUIRED_FIELDS = ("kb_id", "title", "domain", "updated")


def rel(path: Path) -> str:
    """相对仓库根的 POSIX 路径，用于所有对外输出。"""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def unquote(value: str) -> str:
    quote = chr(34)
    if len(value) >= 2 and value[0] == value[-1] == quote:
        return value[1:-1]
    return value


def parse_value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [] if not inner else [unquote(part.strip()) for part in inner.split(",")]
    return unquote(raw) if raw else None


def frontmatter(text: str) -> tuple[dict[str, object], str]:
    """解析 Frontmatter 的扁平子集，返回 (元数据, 去头正文)。

    只支持规范用到的形态：标量、行内列表、短横线多行列表。完整 YAML 依赖在本机
    装不上，所以遇到不支持的语法直接报错，而不是静默跳过——静默会让 domain/tags
    预过滤悄悄失效，比明确失败更难排查。
    """
    lines = text.split(NL)
    if not lines or lines[0].strip() != "---":
        raise ValueError("缺少 YAML Frontmatter（文件必须以 --- 开头）")
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        raise ValueError("Frontmatter 未闭合（缺少第二个 --- 行）")
    meta: dict[str, object] = {}
    key = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line[0] in SPACES:
            if key is None or not line.strip().startswith("-"):
                raise ValueError("Frontmatter 不支持的缩进行：" + repr(line))
            bucket = meta.setdefault(key, [])
            if isinstance(bucket, list):
                bucket.append(unquote(line.strip()[1:].strip()))
            continue
        if ":" not in line:
            raise ValueError("Frontmatter 缺少冒号：" + repr(line))
        key, raw = (part.strip() for part in line.split(":", 1))
        meta[key] = parse_value(raw)
    return meta, NL.join(lines[end + 1:])


def iter_lines(body: str):
    """按行产出 (行号, 行, 是否处于代码围栏内)，围栏内的伪标题不参与切分。"""
    inside = False
    marker = ""
    size = 0
    for number, line in enumerate(body.split(NL), 1):
        fence = FENCE_RE.match(line.strip())
        if fence:
            token = fence.group(1)
            if not inside:
                inside = True
                marker, size = token[0], len(token)
            elif token[0] == marker and len(token) >= size:
                inside = False
        yield number, line, inside


def headings(body: str) -> list[tuple[int, int, str]]:
    """返回 (行号, 层级, 标题文本)，跳过代码块内部。"""
    out = []
    for number, line, inside in iter_lines(body):
        if inside:
            continue
        match = HEADING_RE.match(line)
        if match:
            out.append((number, len(match.group(1)), match.group(2).strip()))
    return out


def estimate_tokens(text: str) -> int:
    """CJK 每字算 1 令牌，拉丁标识符每 4 字符算 1 令牌（向上取整）。"""
    wide = 0
    for ch in text:
        code = ord(ch)
        if 0x3000 <= code <= 0x9fff or 0xAC00 <= code <= 0xD7AF or unicodedata.east_asian_width(ch) in ("W", "F"):
            wide += 1
    latin_chars = sum(len(m.group(0)) for m in WORD_RE.finditer(text))
    return wide + -(-latin_chars // 4)


def content_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def list_knowledge_files(branch: str | None = None) -> list[Path]:
    """列出知识文件，并标注每个文件属于哪个分支。

    规范里 domains/ 和 branches/main/ 有歧义（同一份知识不可能同时躺在两处），
    这里按最小代价落地：domains/ 就是 main 分支的物理位置（第 4 节案例也正是落在这里），
    branches/<name>/ 承载非 main 分支。这样既不留空壳目录，也不需要为每个分支复制整棵树。
    """
    roots = [(DOMAINS_ROOT, DEFAULT_BRANCH), (BRANCHES_ROOT, None)]
    out: list[Path] = []
    for root, fixed_branch in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name.startswith("_"):
                continue
            name = branch_of(path)
            if branch in (None, name):
                out.append(path)
    return out


def branch_of(path: Path) -> str:
    """由物理位置推断分支：branches/<name>/... 归 <name>，其余归 main。"""
    if BRANCHES_ROOT in path.parents:
        relative = path.relative_to(BRANCHES_ROOT)
        if relative.parts:
            return relative.parts[0]
    return DEFAULT_BRANCH


def list_branches() -> list[str]:
    """返回实际存在的分支名（main 始终在列，即使还没有非 main 目录）。"""
    names = {DEFAULT_BRANCH}
    if BRANCHES_ROOT.is_dir():
        names.update(d.name for d in BRANCHES_ROOT.iterdir() if d.is_dir())
    return sorted(names)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + NL
    path.write_bytes(text.encode("utf-8"))


def read_json(path: Path, default: object = None) -> object:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "FAIL  索引产物损坏：" + rel(path) + "（" + str(exc) + "）；删除 "
            + rel(INDEX_DIR) + " 后重跑 indexer"
        )


def configure_stdout() -> None:
    """Windows 控制台默认 GBK，不重配置时中文输出会抛 UnicodeEncodeError。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def as_int_list(value: object) -> list[int]:
    out = []
    for item in as_list(value):
        try:
            out.append(int(item))
        except ValueError:
            pass
    return out