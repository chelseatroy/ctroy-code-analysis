"""MCP server exposing code review tools and prompts."""

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import Tool as MCPTool

from ctroy_code_analysis.instructions import (
    COHESION_REVIEW_INSTRUCTIONS,
    COMMENT_REVIEW_INSTRUCTIONS,
    FULL_DESCRIPTIONS,
    GRIDMAT_INSTRUCTIONS,
    MINIMAL_DESCRIPTIONS,
    NAME_REVIEW_INSTRUCTIONS,
    PERFORMANCE_REVIEW_INSTRUCTIONS,
    TEST_COVERAGE_INSTRUCTIONS,
)


class ProgressiveDisclosureMCP(FastMCP):
    """FastMCP subclass that returns minimal tool descriptions in list_tools()."""

    async def list_tools(self) -> list[MCPTool]:
        tools = self._tool_manager.list_tools()
        return [
            MCPTool(
                name=info.name,
                description=MINIMAL_DESCRIPTIONS.get(info.name, info.description),
                inputSchema=info.parameters,
            )
            for info in tools
        ]


mcp = ProgressiveDisclosureMCP("ctroy-code-analysis")


@mcp.resource("ctroy://tool-descriptions/{tool_name}")
def get_tool_description(tool_name: str) -> str:
    """Return the full description for a tool."""
    if tool_name not in FULL_DESCRIPTIONS:
        return f"Unknown tool: {tool_name}"
    return FULL_DESCRIPTIONS[tool_name]


# ---------------------------------------------------------------------------
# Tools — accept a filepath (or directory), read content, return it with
# review instructions for the LLM to act on.
# ---------------------------------------------------------------------------

@mcp.tool()
def review_comments(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify superfluous and misleading comments."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{COMMENT_REVIEW_INSTRUCTIONS}"


@mcp.tool()
def review_names(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify unclear, mismatched, or shadowed names."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{NAME_REVIEW_INSTRUCTIONS}"


@mcp.tool()
def review_cohesion(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify scattered related logic that should be colocated."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{COHESION_REVIEW_INSTRUCTIONS}"


@mcp.tool()
def review_performance(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify unnecessary computation and inefficient algorithms."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{PERFORMANCE_REVIEW_INSTRUCTIONS}"


@mcp.tool()
def review_test_coverage(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify untested code paths and suggest missing tests."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{TEST_COVERAGE_INSTRUCTIONS}"


@mcp.tool()
def draw_gridmat(directory: str) -> str:
    """List a directory's file structure and return it with instructions to draw an ASCII execution-path diagram with emoji-coded entry points."""
    lines = []
    root = Path(directory)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(".") and d != "__pycache__"
        )
        depth = Path(dirpath).relative_to(root).parts
        indent = "  " * len(depth)
        lines.append(f"{indent}{Path(dirpath).name}/")
        for fname in sorted(filenames):
            if not fname.startswith("."):
                lines.append(f"{indent}  {fname}")

    listing = "\n".join(lines)
    return (
        f"Directory structure of `{directory}`:\n"
        f"```\n{listing}\n```\n\n"
        f"{GRIDMAT_INSTRUCTIONS}"
    )


# ---------------------------------------------------------------------------
# Prompts — return just the review instruction template referencing the
# filepath, so the LLM applies it to code already in context.
# ---------------------------------------------------------------------------

@mcp.prompt()
def prompt_review_comments(filepath: str) -> str:
    """Prompt template for reviewing comments in a source file."""
    return (
        f"Please review the file at `{filepath}` for comment quality.\n\n"
        f"{COMMENT_REVIEW_INSTRUCTIONS}"
    )


@mcp.prompt()
def prompt_review_names(filepath: str) -> str:
    """Prompt template for reviewing names in a source file."""
    return (
        f"Please review the file at `{filepath}` for naming quality.\n\n"
        f"{NAME_REVIEW_INSTRUCTIONS}"
    )


@mcp.prompt()
def prompt_review_cohesion(filepath: str) -> str:
    """Prompt template for reviewing cohesion in a source file."""
    return (
        f"Please review the file at `{filepath}` for cohesion issues.\n\n"
        f"{COHESION_REVIEW_INSTRUCTIONS}"
    )


@mcp.prompt()
def prompt_review_performance(filepath: str) -> str:
    """Prompt template for reviewing performance in a source file."""
    return (
        f"Please review the file at `{filepath}` for performance issues.\n\n"
        f"{PERFORMANCE_REVIEW_INSTRUCTIONS}"
    )


@mcp.prompt()
def prompt_review_test_coverage(filepath: str) -> str:
    """Prompt template for reviewing test coverage of a source file."""
    return (
        f"Please review the file at `{filepath}` for test coverage gaps.\n\n"
        f"{TEST_COVERAGE_INSTRUCTIONS}"
    )


@mcp.prompt()
def prompt_draw_gridmat(directory: str) -> str:
    """Prompt template for drawing a gridmat diagram of a directory."""
    return (
        f"Please draw an execution-path diagram for the codebase at "
        f"`{directory}`.\n\n"
        f"{GRIDMAT_INSTRUCTIONS}"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
