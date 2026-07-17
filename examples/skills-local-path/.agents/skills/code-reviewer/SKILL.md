---
name: code-reviewer
description: Review code for best practices, potential bugs, security issues,
  and provide structured, actionable feedback with severity ratings.
---

# Code Reviewer

## When to use

The user asks you to review code, audit a codebase, check for bugs, or evaluate
code quality. Use this skill whenever the request involves analyzing source code
and providing feedback.

## Workflow

Execute these steps in order. Do not skip any.

### 1. Understand the scope

Identify what code needs to be reviewed:
- A single file, a directory, or a specific function/class.
- If the user does not specify, ask them to clarify the scope.

### 2. Read the code

Use filesystem tools to read the relevant files. Read the entire file(s) — do
not skim or skip sections.

### 3. Analyze against these categories

For each category, flag issues with a severity rating:

| Severity | Meaning |
|----------|---------|
| 🔴 Critical | Security vulnerability, data loss risk, or will cause runtime failure |
| 🟠 High | Bug that produces incorrect results under common conditions |
| 🟡 Medium | Code smell, maintainability issue, or potential future bug |
| 🟢 Low | Style nit, minor improvement, or suggestion |

**Categories to check:**

- **Security**: SQL injection, XSS, hardcoded secrets, unsafe deserialization,
  missing input validation, path traversal, insecure permissions.
- **Correctness**: Off-by-one errors, null/undefined handling, race conditions,
  incorrect error handling, type mismatches.
- **Performance**: N+1 queries, unnecessary allocations, blocking I/O in hot
  paths, missing indexes, inefficient algorithms.
- **Maintainability**: Duplicated code, overly complex functions, magic numbers,
  missing documentation, inconsistent naming, tight coupling.
- **Error Handling**: Missing try/catch, swallowed exceptions, unclear error
  messages, no retry/fallback logic.

### 4. Produce the review

Use the exact output format below. Do not include any other prose or thinking.

## Output format

```
## Code Review — <file-or-scope>

**Summary:** <1-2 sentence overall assessment>

### Issues Found

<For each issue, use this format:>

<#> 🔴/🟠/🟡/🟢 **<Category>** — Line <line_number>
**Issue:** <clear description of the problem>
**Fix:** <specific, actionable suggestion>

### Positive Highlights

- <thing done well>
- <thing done well>

### Recommendations

1. <actionable recommendation>
2. <actionable recommendation>
```

If no issues are found, replace the `### Issues Found` section with:

```
### Issues Found

No issues detected. Code looks clean and well-structured.
```

## Notes / Limitations

- This skill provides static analysis guidance only. It cannot execute or test
  the code.
- Review is limited to the files the agent can access via the filesystem.
- Language-specific best practices should be applied based on the file extension
  and context.
