#!/usr/bin/env python3
"""post-render hook: add `defer` to mermaid <script> tags so they don't block first paint.

Quarto passes the output directory (e.g. _book) as the first argument; the working
directory is the project root. Falls back to _book when no argument is given.
Idempotent: re-running does not add a second `defer`.
"""
import re
import sys
from pathlib import Path

out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_book")
if not out_dir.exists():
    out_dir = Path("_book")

_pattern = re.compile(r'(<script src="[^"]*mermaid[^"]*")>(?=</script>)')

changed = 0
for path in out_dir.rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    new_html = _pattern.sub(r"\1 defer>", html)
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        changed += 1

print(f"defer-mermaid: deferred mermaid scripts in {changed} file(s)")
