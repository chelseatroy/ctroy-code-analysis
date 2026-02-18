"""Review instruction templates and tool description mappings."""

# ---------------------------------------------------------------------------
# Progressive disclosure: minimal descriptions shown in tool listing,
# full descriptions available via resource template.
# ---------------------------------------------------------------------------

MINIMAL_DESCRIPTIONS = {
    "review_comments": "Find superfluous and inaccurate comments",
    "review_names": "Find unclear, mismatched, or shadowed names",
    "review_cohesion": "Find scattered logic that should be colocated",
    "review_performance": "Find inefficient algorithms and unnecessary work",
    "review_test_coverage": "Find untested code paths and suggest tests",
    "draw_gridmat": "Draw ASCII execution-path diagram of a directory",
}

FULL_DESCRIPTIONS = {
    "review_comments": (
        "Read a source file and return its contents with instructions to "
        "identify superfluous and misleading comments.\n\n"
        "Looks for two categories:\n"
        "1. Superfluous comments — the code beneath clearly states what the comment says\n"
        "2. Inaccurate comments — the comment does NOT match what the code actually does\n\n"
        "Findings ordered by severity (inaccurate before superfluous). "
        "Output includes location, problem description, and suggested alternatives."
    ),
    "review_names": (
        "Read a source file and return its contents with instructions to "
        "identify unclear, mismatched, or shadowed names.\n\n"
        "Looks for five categories:\n"
        "1. Unclear names\n"
        "2. Inaccurate names\n"
        "3. Shadowed variables\n"
        "4. Overloaded temporaries\n"
        "5. Low-confidence blocks\n\n"
        "Findings ordered by severity (misleading before vague). "
        "Output includes location, problem description, and name suggestions."
    ),
    "review_cohesion": (
        "Read a source file and return its contents with instructions to "
        "identify scattered related logic that should be colocated.\n\n"
        "Looks for: distant configuration, split validation, fragmented types, "
        "separated tests, dispersed error handling, remote utilities, "
        "disconnected docs, scattered state, split domain logic, orphaned deps.\n\n"
        "Output includes scattered elements, impact explanation, "
        "colocation suggestions, and before/after examples."
    ),
    "review_performance": (
        "Read a source file and return its contents with instructions to "
        "identify unnecessary computation and inefficient algorithms.\n\n"
        "Analyzes five categories:\n"
        "1. Algorithmic complexity\n"
        "2. Data structure efficiency\n"
        "3. Unnecessary work\n"
        "4. I/O and external operations\n"
        "5. Language-specific optimizations\n\n"
        "Output includes current complexity, recommendation, "
        "expected improvement, and tradeoffs."
    ),
    "review_test_coverage": (
        "Read a source file and return its contents with instructions to "
        "identify untested code paths and suggest missing tests.\n\n"
        "Checks: happy paths, branch coverage, edge cases, error paths, "
        "boundary conditions, integration points, return values, "
        "state changes, and concurrency concerns.\n\n"
        "Output includes coverage analysis table and suggested test code."
    ),
    "draw_gridmat": (
        "List a directory's file structure and return it with instructions "
        "to draw an ASCII execution-path diagram with emoji-coded entry points.\n\n"
        "Chooses up to 5 entry points, assigns distinctive emoji, "
        "traces execution paths with fully qualified names and descriptions, "
        "connected with box-drawing characters."
    ),
}

# ---------------------------------------------------------------------------
# Review instruction templates
# ---------------------------------------------------------------------------

COMMENT_REVIEW_INSTRUCTIONS = """\
Review the code for comment quality. Identify two categories of problems:

1. **Superfluous comments** — the code beneath clearly states what the \
comment says.
2. **Inaccurate comments** — the comment does NOT match what the code \
actually does.

List problems in descending order of severity (inaccurate before superfluous).
Consider historical/legal context and platform quirks before flagging.
Do NOT make any changes — suggestions only.

For each problematic comment, output:

### Comment: `"the problematic comment text"`
**Location:** [File and line number]
**Problem:** One sentence explaining why this comment is problematic.
**Recommendation:** Remove or Replace
**Suggested alternatives** (if Replace):
- `// alternative comment 1`
- `// alternative comment 2`
"""

NAME_REVIEW_INSTRUCTIONS = """\
Review the code for naming quality in classes, functions, variables, \
parameters, and constants. Identify these categories of problems:

1. **Unclear names** — don't provide a clear label for what they represent.
2. **Inaccurate names** — don't match what the code actually does.
3. **Shadowed variables** — local names that shadow outer-scope names.
4. **Overloaded temporaries** — generic names like `tmp`, `i`, `x`, `val` \
reused across unrelated blocks.
5. **Low-confidence blocks** — names that reduce confidence in understanding \
code functionality.

List in descending order of severity. Prioritize misleading names over vague \
ones. Respect codebase and language conventions. Do NOT perform renames — \
suggestions only.

For each problematic name, output:

### [Name]: `the_problematic_name`
**Location:** [File and line number]
**Problem:** One sentence explaining why this name is problematic.
**Suggestions:**
- `alternative_name_1`
- `alternative_name_2`
- `alternative_name_3`
"""

COHESION_REVIEW_INSTRUCTIONS = """\
Review the code for cohesion issues — when related pieces of information, \
logic, or configuration are scattered across the codebase instead of \
colocated. A developer should find everything related to a single concept \
in one place or clearly related nearby files.

Signs of poor cohesion to look for:
1. Distant Configuration — settings far from usage
2. Split Validation — validation rules scattered across files
3. Fragmented Type Definitions — related types in separate locations
4. Separated Tests — tests organized by type rather than colocated with code
5. Dispersed Error Handling — error types/messages spread across codebase
6. Remote Utilities — helper functions in generic utility folders
7. Disconnected Documentation — docs far from code
8. Scattered State Management — state/reducers/actions in different trees
9. Split Domain Logic — business rules across multiple modules
10. Orphaned Dependencies — imports from many distant locations

Review process:
1. Identify Core Concepts
2. Trace Dependencies (config, types, validation, tests, utilities, docs)
3. Measure Scatter (how many locations must a developer visit?)
4. Assess Change Impact (how many files need modification for one change?)
5. Propose Colocation (specific reorganization recommendations)

For each issue, output:

### Issue: [Brief Description]
**Scattered Elements:**
- List the files/locations where related pieces are spread

**Why This Matters:**
- Explain cognitive load or maintenance burden

**Suggested Colocation:**
- Specific recommendation for reorganization
- Include proposed file/folder structure

**Example Change:**
- Brief before/after

Prioritize scattering that genuinely hurts understandability. Respect \
existing architectural boundaries. Suggest incremental improvements, not \
wholesale rewrites.
"""

PERFORMANCE_REVIEW_INSTRUCTIONS = """\
Review the code for performance optimization opportunities. Analyze across \
five categories:

1. **Algorithmic Complexity** — identify Big O complexity, nested loops that \
could be flattened, O(n²) or worse patterns, memoization opportunities, \
unnecessary sorting/searching.

2. **Data Structure Efficiency** — evaluate data structure choices for access \
patterns, find O(1) lookup opportunities (sets/dicts vs lists), identify \
generator opportunities, check for unnecessary copying/conversion.

3. **Unnecessary Work** — find computations that could be hoisted outside \
loops, redundant operations, early-exit opportunities, over-fetching or \
over-processing.

4. **I/O and External Operations** — identify N+1 query patterns, batching \
opportunities, missing caching, sync operations that could be parallelized.

5. **Language-Specific Optimizations** — recommend faster built-in functions, \
identify anti-patterns, suggest more efficient idioms.

Report genuine optimization opportunities, not micro-optimizations. Prioritize \
by expected impact (high/medium/low). Be quantitative where possible.

For each issue, output:

### Issue: [Brief description]
**Location:** [File and line numbers or code snippet]
**Current Complexity:** [Time/space complexity if relevant]
**Problem:** [Clear explanation of inefficiency]
**Recommendation:** [Specific code changes]
**Expected Improvement:** [Estimated performance gain]
**Tradeoffs:** [Memory, CPU, code complexity, or other impacts]
"""

TEST_COVERAGE_INSTRUCTIONS = """\
Review the code and identify untested code paths. Check for:

- Happy paths (normal/expected inputs and outputs)
- Branch coverage (every if/elif/else, case in match)
- Edge cases (empty, None, boundary values, min/max)
- Error paths (exception handling, invalid inputs)
- Boundary conditions (off-by-one, empty collections)
- Integration points
- Return values
- State changes and side effects
- Concurrency concerns

For each gap found, suggest a test. Use descriptive method names like \
`test_validate_email_rejects_missing_at_sign`. Include both positive and \
negative cases.

Output:

### Coverage Analysis
| Code Path / Construct | File:Line | Existing Test? | Gap Description |
|---|---|---|---|
| ... | ... | ... | ... |

### Suggested Tests
For each missing test, provide:
- The test code
- What code path it covers
- Why this coverage was missing
"""

GRIDMAT_INSTRUCTIONS = """\
Using the directory listing, draw an ASCII execution-path diagram:

1. Choose up to 5 example entry points from this codebase.
2. Pick an emoji with a distinctive color to represent each entry point.
3. Place the entry points at the top of the diagram.
4. Trace execution paths downward into implementation files.
5. Include fully qualified names and ~20 word descriptions of what happens \
at each level.
6. Use box-drawing characters to connect the paths.

The result should give a reader a quick mental model of how the major \
code paths flow through this codebase.
"""
