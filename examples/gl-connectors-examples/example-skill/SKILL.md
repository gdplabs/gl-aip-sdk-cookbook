---
name: pr-monthly-summary
description: Summarize pull requests from a GitHub repository for the current
  calendar month, upload a CSV report to the user's Google Drive, and respond
  with a formatted summary.
---

# PR Monthly Summary

## When to use

The user asks for a summary of pull requests from a GitHub repository scoped
to "this month", "the current month", or a similar phrasing.

## Available tools (and the only ones you may use)

- `get_month_date_range` — returns `{ "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }` for the current UTC month.
- `github_list_pull_requests` — GL Connectors GitHub MCP. Lists PRs with cursor pagination.
- `write_temp_file` — writes text content to `/tmp/<filename>` and returns the absolute path.
- `google_drive_upload_file_api` — uploads a local file to the caller's Google Drive (My Drive root).
- `delete_file` — deletes a local file.

## Workflow

Execute these steps in order. Do not skip any.

### 1. Get the month window

Call `get_month_date_range`. Capture `start` and `end` (both `YYYY-MM-DD`).

### 2. List PRs in the window

Call `github_list_pull_requests` with:

- `owner = "gdplabs"`
- `repo = "gl-aip-sdk-cookbook"`
- `states = ["OPEN", "CLOSED", "MERGED"]`
- `order_by = "CREATED_AT"`
- `direction = "DESC"`
- `per_page = 100`

Paginate forward using the `cursor` field returned in the response's `meta.forwards_cursor`
while `meta.has_next` is true. Stop early once a page's oldest PR has
`created_at` strictly before `start` — no further pages can contain in-window PRs.

Keep only PRs where `created_at` falls within `[start 00:00:00 UTC, end 23:59:59 UTC]` inclusive.

### 3. Build CSV rows

For each kept PR, derive these fields (CSV column order is fixed):

| Column     | Source                                                                  |
|------------|-------------------------------------------------------------------------|
| PR Link    | `url`                                                                   |
| PR Title   | `title`                                                                 |
| Assignee   | `assignees[0]` if present, else `N/A`                                   |
| PR Status  | `"merged"` if `merged_at` is not null; else lowercase `state` (`open`/`closed`) |

Quote any field containing `,`, `"`, or a newline using RFC 4180 rules
(wrap in double quotes, escape inner `"` as `""`).

### 4. Write the temp CSV

Call `write_temp_file` with:

- `filename`: `prs_gl-aip-sdk-cookbook_<YYYY-MM>.csv` (use the month from `start`).
- `content`: a CSV starting with the header line:

  ```
  PR Link,PR Title,Assignee,PR Status
  ```

  followed by one row per kept PR.

Capture the returned absolute path as `temp_path`.

### 5. Upload to Google Drive

Call `google_drive_upload_file_api` with:

- `path = temp_path`
- `content_type = "text/csv"`

The file lands in the user's My Drive root (no parent folder is set). Capture the
returned file `id` (and `name`) for the final response.

### 6. Delete the temp file

Call `delete_file` with `path = temp_path`. Do this regardless of whether the
upload succeeded.

### 7. Respond

Use the exact output format below. Do not include any other prose or thinking.

## Output format

```
## Monthly PR Summary — gdplabs/gl-aip-sdk-cookbook

**Window:** <start> → <end>
**Total PRs:** <N>  ·  **Open:** <O>  ·  **Closed:** <C>  ·  **Merged:** <M>

### Pull Requests
1. [<PR Title>](<PR Link>) — `<status>` — Assignee: @<login or N/A>
2. ...

### Report
Uploaded `<filename>` to Google Drive (file id: `<id>`).
```

If `Total PRs` is 0, omit the numbered list and replace the `### Pull Requests`
section with the single line:

```
No pull requests were created this month.
```

## Notes / Limitations

- The GL Connectors GitHub plugin's `list_pull_requests` schema does not expose
  reviewer information, so reviewer columns are intentionally absent from the
  CSV and the response.
- All date math is UTC. A PR opened late on the last day of the month in a
  westward timezone may still count as in-window here.
