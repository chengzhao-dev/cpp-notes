#!/usr/bin/env python3
"""检查受管目录中的空文件与空目录。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKIP = {".git", "_book", ".quarto", ".cache", ".tmp", "build", "temp"}


def main() -> int:
    empty_files = []
    empty_dirs = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_file() and path.stat().st_size == 0:
            empty_files.append(rel.as_posix())
        elif path.is_dir() and not any(path.iterdir()):
            empty_dirs.append(rel.as_posix())
    if empty_files or empty_dirs:
        print(f"FAIL  empty  files={len(empty_files)} dirs={len(empty_dirs)}")
        for item in empty_files + empty_dirs:
            print(f"      {item}")
        return 1
    print("PASS  empty  no empty files or directories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
