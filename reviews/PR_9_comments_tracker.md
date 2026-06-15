# PR 9 Review Comments

## Comments Summary
- **Open** 5
- **Fixed** 6
- **Wont Fixed** 0
- **Total** 11

--

## Comment List

### 1. [H-1] Missing `load_dotenv()` before env checks
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/01_local_eval.py`
- **Line:** 30
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373648
- **Status:** `FIXED`
- **Priority:** High
- **Summary:** `01_local_eval.py` checks `os.getenv("OPENAI_API_KEY")` but never calls `load_dotenv()`, so the documented quickstart (`cp .env.example .env` then `uv run python 01_local_eval.py`) fails unless the user manually exports the variable. Same issue applies to `02_remote_eval.py` for `OPENAI_API_KEY`, `AIP_API_URL`, and `AIP_API_KEY`.
- **Fix:** Added `load_dotenv()` as the first line of `main()` in both `01_local_eval.py` and `02_remote_eval.py`. Local eval re-verified and passes (1/1, all 4 metrics).

### 2. [L-1] Link cookbook from root README examples list
- **Author:** raychrisgdp
- **File:** `README.md`
- **Line:** 11
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#pullrequestreview-4482057730
- **Status:** `FIXED`
- **Priority:** Low
- **Summary:** The new `examples/aip-evals/` cookbook should be linked from the root repository README's examples list so users can discover it from the landing page.
- **Fix:** Added `aip-evals` to the "Local-run flows" list in the root README's Examples section.

### 3. [M-1] Misleading "no external API dependencies" claim
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/README.md`
- **Line:** 3
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373650
- **Status:** `FIXED`
- **Priority:** Medium
- **Summary:** The README intro says the cookbook "can be run without any external API dependencies" but the quickstart and YAML test case require `OPENAI_API_KEY` for model-based metrics. The claim should be narrowed to say the mocked search tool avoids a real search API, while model-based evals still require OpenAI credentials.
- **Fix:** Narrowed the intro to clarify the no-API claim applies only to the mocked search tool, and added a note that model-based metrics still require `OPENAI_API_KEY`.

### 4. [M-2] Python 3.12 constraint not documented
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/pyproject.toml`
- **Line:** 5
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373656
- **Status:** `FIXED`
- **Priority:** Medium
- **Summary:** `pyproject.toml` requires `requires-python = ">=3.12"`, but the repo root README says users can install Python 3.11 or 3.12. The cookbook should either relax to 3.11 if evals support it, or explicitly document "Requires Python 3.12" in the cookbook's README.
- **Fix:** Verified `gllm-core-binary 0.4.28` only ships `cp312` wheels, so the 3.12 constraint is forced by the SDK's native binary deps. Added a "Prerequisites" section to the cookbook README explicitly calling out Python 3.12.

### 5. [M-3] Unused `psycopg2-binary` and outdated project description
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/pyproject.toml`
- **Line:** 10
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373660
- **Status:** `FIXED`
- **Priority:** Medium
- **Summary:** `psycopg2-binary` is listed as a dependency but is not imported or used by the research-agent example. The project description also mentions "python" metrics even though the test case only uses deterministic and model metrics. This is leftover baggage from the older PDRB scope.
- **Fix:** Removed `psycopg2-binary` from `pyproject.toml` dependencies and updated the project description to "Demonstrate AIP evals module — evaluate local and hosted agents using deterministic and model metrics". Refreshed `uv.lock` to drop the unused package.

### 6. [Q-1] PR body outdated (describes Lokadata/PDRB, diff is research agent)
- **Author:** raychrisgdp
- **File:** (PR description)
- **Line:** —
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#pullrequestreview-4482062035
- **Status:** `FIXED`
- **Priority:** Medium
- **Summary:** The live PR description at review time described the old Lokadata/PDRB cookbook with three eval scripts, but the diff adds the new research-agent cookbook with two eval scripts. Questioned whether the description needs updating or the wrong files were replaced.
- **Fix:** PR description was updated during the session to reflect the new research-agent scope.

### 7. [D-1] Missing docstring in 01_local_eval.py
- **Author:** chen-gdp
- **File:** `examples/aip-evals/01_local_eval.py`
- **Line:** 31
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3407463096
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** Reminds to add/verify the module docstring for `01_local_eval.py`.
- **Fix:**

### 8. [D-2] Missing docstring in 02_remote_eval.py
- **Author:** chen-gdp
- **File:** `examples/aip-evals/02_remote_eval.py`
- **Line:** 31
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3407463359
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** Same reminder — add/verify the module docstring for `02_remote_eval.py`.
- **Fix:**

### 9. [C-1] Add pre-commit.yaml for formatting
- **Author:** chen-gdp
- **File:** `examples/aip-evals/agents/__init__.py`
- **Line:** —
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3407464163
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** Suggests adding a `pre-commit.yaml` configuration file to the parent `examples/` folder so all code is auto-formatted consistently.
- **Fix:**

### 10. [C-2] Remove reviews tracker from PR
- **Author:** chen-gdp
- **File:** `reviews/PR_9_comments_tracker.md`
- **Line:** —
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3407464361
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** Notes that the reviews tracker doc should not be pushed to the PR — it's an internal working artifact, not part of the cookbook.
- **Fix:**

### 11. [C-3] Add gitbook reference to README
- **Author:** chen-gdp
- **File:** `examples/aip-evals/README.md`
- **Line:** 102
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3407465158
- **Status:** `OPEN`
- **Priority:** Low
- **Summary:** Suggests adding a reference/link to the GL AIP gitbook for more information about the evals module.
- **Fix:**
