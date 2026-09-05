#!/usr/bin/env python3
"""检查仓库文本的 UTF-8、BOM、行尾和常见乱码特征。"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "_book", ".quarto", "build", "node_modules"}
TEXT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".css", ".h", ".hpp", ".html", ".json", ".md",
    ".qmd", ".py", ".qmd", ".sh", ".toml", ".txt", ".yml", ".yaml",
}
TEXT_NAMES = {".editorconfig", ".gitignore", ".gitattributes", "AGENTS.md", "README.md"}
MOJIBAKE_MARKERS = ("锟", "鏂", "鐜", "绔", "鎴", "璇", "浠", "鍏", "瀹", "閸")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def is_text_candidate(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix.lower() in TEXT_EXTENSIONS


def suspicious(text: str) -> bool:
    if "\ufffd" in text or any(0xE000 <= ord(ch) <= 0xF8FF for ch in text):
        return True
    # 错误地用 GBK 解码再写回 UTF-8 时，通常会出现连续的这些标记字符。
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS) >= 4


def main() -> int:
    failures = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or is_skipped(path) or not is_text_candidate(path):
            continue
        rel = path.relative_to(ROOT)
        if rel == Path("scripts/agent/check_encoding.py"):
            continue
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{rel}: 非 UTF-8（字节 {exc.start}）")
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            failures.append(f"{rel}: 含 UTF-8 BOM")
        if b"\r\n" in raw or b"\r" in raw:
            failures.append(f"{rel}: 含 CRLF/CR 行尾，应统一为 LF")
        if suspicious(text):
            line = next((i for i, value in enumerate(text.splitlines(), 1) if suspicious(value)), 1)
            failures.append(f"{rel}:{line}: 疑似乱码，请以 UTF-8 无 BOM 重新保存")

    if failures:
        print("FAIL encoding")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print("PASS encoding UTF-8 无 BOM、LF、无明显乱码")
    return 0


if __name__ == "__main__":
    sys.exit(main())
