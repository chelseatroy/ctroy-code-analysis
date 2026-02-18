# ctroy-code-analysis

An MCP server that provides six code review tools for use with Claude Code
(or any MCP client). Each reviewer reads a file from disk, pairs its contents
with a structured review prompt, and returns the bundle for the LLM to
evaluate.

## Installation

```bash
pip install ctroy-code-analysis
```

Requires Python 3.10+.

## Connecting to Claude Code

Add the server to your project's `.mcp.json` (per-project) or
`~/.claude.json` (global):

```json
{
  "mcpServers": {
    "ctroy-code-analysis": {
      "command": "ctroy-code-analysis"
    }
  }
}
```

Restart Claude Code. The six tools will appear automatically.

## Tools

Each tool takes a filepath (or directory), reads the contents, and returns
them alongside review instructions. The LLM then generates the review.

| Tool | Input | What It Reviews |
|------|-------|-----------------|
| `review_comments` | `filepath` | Identifies superfluous comments that restate obvious code and inaccurate comments that contradict what the code does. |
| `review_names` | `filepath` | Identifies unclear, inaccurate, or shadowed names in classes, functions, variables, and constants. |
| `review_cohesion` | `filepath` | Identifies related logic scattered across the codebase that should be colocated. |
| `review_performance` | `filepath` | Identifies unnecessary computation, inefficient algorithms, and missed optimization opportunities. |
| `review_test_coverage` | `filepath` | Identifies untested code paths including edge cases, error paths, and boundary conditions. |
| `draw_gridmat` | `directory` | Lists the directory structure and produces an ASCII execution-path diagram with emoji-coded entry points. |

### Example usage in Claude Code

Ask Claude naturally:

```
Use review_comments on src/parser.py
```

```
Use review_performance on lib/data_pipeline.py
```

```
Use draw_gridmat on the src/ directory
```

## Prompts

Each tool also has a corresponding prompt (prefixed with `prompt_`). Prompts
return just the review instructions without reading any files, so the LLM
applies them to code it already has in context.

| Prompt | Input |
|--------|-------|
| `prompt_review_comments` | `filepath` |
| `prompt_review_names` | `filepath` |
| `prompt_review_cohesion` | `filepath` |
| `prompt_review_performance` | `filepath` |
| `prompt_review_test_coverage` | `filepath` |
| `prompt_draw_gridmat` | `directory` |

## What the reviewers look for

**Comment review** flags two categories, ordered by severity:
inaccurate comments (say something the code doesn't do) and superfluous
comments (restate what the code clearly says).

**Name review** flags five categories: unclear names, inaccurate names,
shadowed variables, overloaded temporaries (`tmp`, `i`, `x` reused across
unrelated blocks), and low-confidence blocks where names make it hard to
reason about the code.

**Cohesion review** looks for ten patterns of scattered code: distant
configuration, split validation, fragmented type definitions, separated
tests, dispersed error handling, remote utilities, disconnected docs,
scattered state management, split domain logic, and orphaned dependencies.

**Performance review** analyzes five categories: algorithmic complexity,
data structure efficiency, unnecessary work, I/O and external operations,
and language-specific optimizations. Each finding includes expected
improvement and tradeoffs.

**Test coverage review** checks for gaps in: happy paths, branch coverage,
edge cases, error paths, boundary conditions, integration points, return
values, state changes, and concurrency concerns.

**Gridmat** picks up to 5 entry points, assigns each a color-coded emoji,
and traces execution paths downward through the codebase in an ASCII
box-drawing diagram.

## Running the server directly

The server uses stdio transport. To start it manually:

```bash
ctroy-code-analysis
```

Or:

```bash
python -m ctroy_code_analysis.server
```
