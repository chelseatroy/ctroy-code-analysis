# Contributing to ctroy-code-analysis

## Setup

1. Clone the repository:

```bash
git clone https://github.com/chelseatroy/ctroy-code-analysis.git
cd ctroy-code-analysis
```

2. Create a virtual environment and install in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

(If the `dev` extras aren't set up yet, just `pip install -e .` works fine.)

3. Verify the server starts:

```bash
python -c "from ctroy_code_analysis.server import mcp; print('OK')"
```

## Project structure

```
ctroy-code-analysis/
├── pyproject.toml                  # Package metadata, dependencies, entry point
├── README.md                       # User-facing documentation
├── CONTRIBUTING.md                 # This file
└── src/
    └── ctroy_code_analysis/
        ├── __init__.py
        └── server.py               # All tools, prompts, and review instructions
```

Everything lives in `server.py`. The file has three sections:

1. **Instruction templates** — the `*_INSTRUCTIONS` constants at the top.
   These are the review prompts that get returned to the LLM.
2. **Tools** — `@mcp.tool()` functions that read a file/directory and return
   its contents concatenated with the relevant instructions.
3. **Prompts** — `@mcp.prompt()` functions that return just the instructions
   (no file reading), for when the LLM already has the code in context.

## Adding a new reviewer

1. Write the instruction template as a module-level constant (e.g.,
   `SECURITY_REVIEW_INSTRUCTIONS`). Follow the pattern of the existing ones:
   describe what to look for, how to prioritize findings, and what output
   format to use.

2. Add a tool function:

```python
@mcp.tool()
def review_security(filepath: str) -> str:
    """Read a source file and return its contents with instructions to identify security issues."""
    content = Path(filepath).read_text()
    return f"File: {filepath}\n```\n{content}\n```\n\n{SECURITY_REVIEW_INSTRUCTIONS}"
```

3. Add a corresponding prompt function:

```python
@mcp.prompt()
def prompt_review_security(filepath: str) -> str:
    """Prompt template for reviewing security in a source file."""
    return (
        f"Please review the file at `{filepath}` for security issues.\n\n"
        f"{SECURITY_REVIEW_INSTRUCTIONS}"
    )
```

4. Test locally by importing and calling the tool function on a real file:

```bash
python -c "
from ctroy_code_analysis.server import review_security
print(review_security('some/file.py')[:200])
"
```

## Testing changes with Claude Code

After making changes, test them with a live Claude Code session:

1. Make sure the package is installed in editable mode (`pip install -e .`).

2. Add to your Claude Code config (`.mcp.json` in any project):

```json
{
  "mcpServers": {
    "ctroy-code-analysis": {
      "command": "ctroy-code-analysis"
    }
  }
}
```

3. Restart Claude Code and ask it to use one of the tools on a file.

## Publishing a new version

1. Bump the version in `pyproject.toml`.

2. Build and upload:

```bash
python -m build
twine upload dist/*
```

This requires a PyPI API token configured in `~/.pypirc`.

## Style guidelines

- Keep all tools and prompts in `server.py` unless the file becomes unwieldy.
- Instruction templates should be specific about output format so the LLM
  produces consistent, structured reviews.
- Tool docstrings should describe what the tool does in one sentence — these
  show up in the MCP tool listing that the LLM sees.
- Each instruction template should order its findings by severity (most
  severe first).
