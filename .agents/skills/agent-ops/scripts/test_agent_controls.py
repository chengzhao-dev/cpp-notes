#!/usr/bin/env python3
"""Agent 编码、MCP 范围读取和安全输出的最小回归测试。"""

from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[4]
sys.dont_write_bytecode = True


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


encoding = load(ROOT / ".agents/skills/agent-ops/scripts/check_encoding.py", "check_encoding")
docs = load(ROOT / ".agents/skills/agent-ops/scripts/check_docs.py", "check_docs")
mcp = load(ROOT / ".agents/mcp/server.py", "mcp_server")
runner = load(ROOT / ".agents/skills/agent-ops/scripts/run.py", "run_agent")
scope = load(ROOT / ".agents/skills/agent-ops/scripts/scope.py", "scope")
size = load(ROOT / ".agents/skills/agent-ops/scripts/check_skill_size.py", "check_skill_size")
verify = load(
    ROOT / ".agents/skills/cpp-content/scripts/verify_examples.py",
    "verify_examples",
)


def main() -> int:
    assert encoding.control_issues("auto\x07") == [(1, 5, "U+0007")]
    assert encoding.control_issues("中文\n\ttext") == []
    assert encoding.suspicious("\u951f" * 4)
    assert encoding.severity(Path(".agents/skills/agent-ops/scripts/x.py")) == "hard"
    assert encoding.severity(Path("content/language-basics/types-and-variables.qmd")) == "hard"

    valid_answer = [
        "   ::: {.answer}",
        "   从源码到程序运行依次经过以下步骤：",
        "   1. 编译源码。",
        "   :::",
    ]
    assert docs.check_answer_disclosures("content/test.qmd", valid_answer) == []
    raw_answer = ['   <details class="legacy answer-disclosure">']
    assert any(
        "DOC-E18" in error
        for error in docs.check_answer_disclosures("content/test.qmd", raw_answer)
    )
    empty_answer = ["   ::: {.answer}", "   :::"]
    assert any(
        "不能为空" in error
        for error in docs.check_answer_disclosures("content/test.qmd", empty_answer)
    )
    list_without_intro = [
        "   ::: {.answer}",
        "   1. 编译源码。",
        "   :::",
    ]
    assert any(
        "DOC-E19" in error
        for error in docs.check_answer_disclosures("content/test.qmd", list_without_intro)
    )
    unindented_answer_body = [
        "   ::: {.answer}",
        "   这是答案导语。",
        "这一行没有保持列表缩进。",
        "   :::",
    ]
    assert any(
        "DOC-E18" in error
        for error in docs.check_answer_disclosures("content/test.qmd", unindented_answer_body)
    )
    fenced_marker = [
        "   ::: {.answer}",
        "   从源码到程序运行依次经过以下步骤：",
        "   ```text",
        "   :::",
        "   ```",
        "   1. 编译源码。",
        "   :::",
    ]
    assert docs.check_answer_disclosures("content/test.qmd", fenced_marker) == []
    assert docs.heading_level_errors("content/test.qmd", [(1, 2, "二级")]) == []
    assert any(
        "DOC-E21" in error
        for error in docs.heading_level_errors("content/test.qmd", [(1, 4, "四级")])
    )
    assert any(
        "DOC-E2" in error
        for error in docs.frontmatter_title_errors(
            "content/test.qmd",
            ["---", 'title: "用 `CMake` 构建"', "---"],
        )
    )
    assert docs.frontmatter_title_errors(
        "content/test.qmd",
        ["---", 'title: "用 CMake 构建"', "---"],
    ) == []
    assert size.effective_content_chars(
        "正文一。\n```{.cpp}\nint main() {}\n```\n{{< include /code/demo.cpp >}}\n正文二。"
    ) == len("正文一。") + len("正文二。")

    assert docs.has_purpose_comment(
        Path("code/sample/main.cpp"),
        ["// 程序入口：输出问候。", "#include <iostream>"],
    )
    assert not docs.has_purpose_comment(
        Path("code/sample/greeting.h"),
        ["#pragma once", "// 接口声明应位于文件开头。"],
    )
    assert docs.has_purpose_comment(
        Path("code/sample/build.sh"),
        ["#!/usr/bin/env bash", "", "# 构建并运行示例。", "set -euo pipefail"],
    )
    assert not docs.has_purpose_comment(
        Path("code/sample/build.sh"),
        ["#!/usr/bin/env bash", "set -euo pipefail"],
    )
    assert docs.has_purpose_comment(
        Path("code/sample/CMakeLists.txt"),
        ["# 构建示例目标。", "cmake_minimum_required(VERSION 3.31)"],
    )
    assert not docs.has_purpose_comment(
        Path("code/sample/CMakeLists.txt"),
        ["cmake_minimum_required(VERSION 3.31)"],
    )
    assert docs.cmake_target_comment_errors(
        ROOT / "code/sample/CMakeLists.txt",
        ["# 创建 app 可执行目标。", "add_executable(app main.cpp)"],
    ) == []
    assert any(
        "DOC-E22" in error
        for error in docs.cmake_target_comment_errors(
            ROOT / "code/sample/CMakeLists.txt",
            ["add_executable(app main.cpp)"],
        )
    )

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
        "query": "run.ps1", "path": "AGENTS.md",
        "maxResults": 1, "contextLines": 1,
    })
    item = search["structuredContent"]["results"][0]
    assert item["line"] > 0 and isinstance(item["before"], list)
    review = next(tool for tool in mcp.TOOLS if tool["name"] == "project_review")
    assert review["inputSchema"]["properties"] == {}
    assert runner.status_group(".agents/skills/catalog.md") == "maintenance"
    assert runner.status_group("knowledge/README.md") == "content"
    changed_cpp = [
        "code/getting-started/first-program/first-program.cpp",
        "code/getting-started/multi-file-project/src/main.cpp",
        "code/getting-started/multi-file-project/include/greeting.h",
        "code/getting-started/multi-file-project/CMakeLists.txt",
        "code/getting-started/static-library/greeting/src/greeting.cpp",
        "code/getting-started/shared-library/CMakeLists.txt",
    ]
    assert set(runner.relevant_cpp_paths(changed_cpp)) == set(changed_cpp)
    assert runner.relevant_cpp_paths(["index.qmd"]) == []
    projects = verify.find_cmake_projects(str(ROOT / "code"))
    assert str(ROOT / "code" / "getting-started" / "multi-file-project") in projects
    assert str(ROOT / "code" / "getting-started" / "cmake-project") in projects
    assert str(ROOT / "code" / "getting-started" / "static-library") in projects
    assert str(ROOT / "code" / "getting-started" / "shared-library") in projects
    assert (ROOT / "code" / "getting-started" / "first-program" / "build-and-run.sh").is_file()
    for name in ("main.cpp", "greeting.h", "greeting.cpp", "build-and-run.sh"):
        assert (ROOT / "code" / "getting-started" / "minimal-program-structure" / name).is_file()
    library_unit = scope.find_chapter_by_code_path(
        ROOT
        / "code"
        / "getting-started"
        / "shared-library"
        / "greeting"
        / "src"
        / "greeting.cpp",
        ROOT,
    )
    assert library_unit["chapter"] == "shared-library"
    assert scope.resolve_repo_domain(
        ".agents/skills/github-ops/SKILL.md", ROOT
    )["label"] == "skill github-ops"
    skill_reads = scope.resolve_repo_domain(
        ".agents/skills/cpp-content/SKILL.md", ROOT
    )["reads"]
    assert skill_reads == [".agents/skills/cpp-content/SKILL.md"]
    maintenance_reads = scope.resolve_repo_domain(
        ".agents/skills/agent-ops/references/refactor-guidelines.md", ROOT
    )["reads"]
    assert ".agents/skills/catalog.md" in maintenance_reads
    assert scope.resolve_repo_domain(
        "knowledge/README.md", ROOT
    )["label"] == "knowledge"
    def headings(path):
        return {
            line.lstrip("#").strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("##")
        }

    plan_reference = ROOT / ".agents/skills/agent-ops/references/plan-artifacts.md"
    plan_text = plan_reference.read_text(encoding="utf-8")
    assert "固定 H2 顺序" in plan_text
    assert "### 交付收口" in plan_text
    assert "<!-- plan-complete -->" in plan_text
    git_workflow = ROOT / ".agents/skills/github-ops/references/git-workflow.md"
    assert "交付收口" in git_workflow.read_text(encoding="utf-8")
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Plan Mode" in agents_text and "交付收口" in agents_text
    assert (ROOT / ".agents/skills/cpp-content/references/cpp/language-basics.md").is_file()
    assert (ROOT / "knowledge/cpp-content/language-basics-path.md").is_file()
    assert (ROOT / "knowledge/agent-ops/scalable-course-maintenance.md").is_file()
    assert runner.display_command("kb-index") == "知识库索引"
    assert runner.display_check("kb-eval") == "知识库评测"
    assert "批准不等于上传完成" in headings(
        ROOT / "knowledge/agent-ops/plan-artifact-source.md"
    )
    tools = {tool["name"]: tool for tool in mcp.TOOLS}
    execution_only = {
        "project_review",
        "project_edit",
        "project_check",
        "project_verify",
        "project_render",
        "project_build",
    }
    for name in execution_only:
        assert "Plan Mode" in tools[name]["description"]
        annotations = tools[name]["annotations"]
        assert annotations["readOnlyHint"] is False
        assert annotations["openWorldHint"] is False
    for name in {"project_status", "project_diff", "project_scope", "project_read", "project_search"}:
        assert tools[name]["annotations"]["readOnlyHint"] is True
    profile_schema = tools["project_check"]["inputSchema"]["properties"]["profile"]
    assert profile_schema["default"] == "full"
    assert "fast" in profile_schema["enum"]
    assert len(runner.checks_for_profile("fast")) < len(runner.checks_for_profile("full"))
    print("通过  Agent 控制检查")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
