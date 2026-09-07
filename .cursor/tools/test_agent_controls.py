#!/usr/bin/env python3
"""Agent 编码、MCP 范围读取和安全输出的最小回归测试。"""

from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


encoding = load(ROOT / ".cursor/tools/check_encoding.py", "check_encoding")
mcp = load(ROOT / ".cursor/mcp/server.py", "mcp_server")


def main() -> int:
    assert encoding.control_issues("auto\x07") == [(1, 5, "U+0007")]
    assert encoding.control_issues("中文\n\ttext") == []
    assert encoding.suspicious("\u951f" * 4)
    assert encoding.severity(Path(".cursor/tools/x.py")) == "hard"
    assert encoding.severity(Path("content/core/intro.qmd")) == "soft"

    assert mcp.redact("API_KEY=secret-value") == "API_KEY=[REDACTED]"
    assert "abc.def-123" not in mcp.redact("Authorization: Bearer abc.def-123")
    assert mcp.redact("sk-1234567890abcdef") == "[REDACTED]"
    result = mcp.tool_result({"text": "token: secret-value"})
    assert "secret-value" not in result["content"][0]["text"]
    try:
        mcp.relative_path(".env")
    except mcp.MCPError:
        pass
    else:
        raise AssertionError(".env must be denied")

    read = mcp.handle_tool("project_read", {"path": "AGENTS.md", "startLine": 1, "endLine": 2})
    assert read["structuredContent"]["startLine"] == 1
    assert read["structuredContent"]["totalLines"] >= 2
    search = mcp.handle_tool("project_search", {
        "query": "简洁优先", "path": "AGENTS.md",
        "maxResults": 1, "contextLines": 1,
    })
    item = search["structuredContent"]["results"][0]
    assert item["line"] > 0 and isinstance(item["before"], list)
    print("PASS agent controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
