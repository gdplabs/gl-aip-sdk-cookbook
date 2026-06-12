# PR 9 Review Comments

## Comments Summary
- **Open** 3
- **Fixed** 3
- **Wont Fixed** 0
- **Total** 6

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
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** The README intro says the cookbook "can be run without any external API dependencies" but the quickstart and YAML test case require `OPENAI_API_KEY` for model-based metrics. The claim should be narrowed to say the mocked search tool avoids a real search API, while model-based evals still require OpenAI credentials.
- **Fix:**

### 4. [M-2] Python 3.12 constraint not documented
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/pyproject.toml`
- **Line:** 5
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373656
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** `pyproject.toml` requires `requires-python = ">=3.12"`, but the repo root README says users can install Python 3.11 or 3.12. The cookbook should either relax to 3.11 if evals support it, or explicitly document "Requires Python 3.12" in the cookbook's README.
- **Fix:**

### 5. [M-3] Unused `psycopg2-binary` and outdated project description
- **Author:** raychrisgdp
- **File:** `examples/aip-evals/pyproject.toml`
- **Line:** 10
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#discussion_r3400373660
- **Status:** `OPEN`
- **Priority:** Medium
- **Summary:** `psycopg2-binary` is listed as a dependency but is not imported or used by the research-agent example. The project description also mentions "python" metrics even though the test case only uses deterministic and model metrics. This is leftover baggage from the older PDRB scope.
- **Fix:**

### 6. [Q-1] PR body outdated (describes Lokadata/PDRB, diff is research agent)
- **Author:** raychrisgdp
- **File:** (PR description)
- **Line:** —
- **URL:** https://github.com/gdplabs/gl-aip-sdk-cookbook/pull/9#pullrequestreview-4482062035
- **Status:** `FIXED`
- **Priority:** Medium
- **Summary:** The live PR description at review time described the old Lokadata/PDRB cookbook with three eval scripts, but the diff adds the new research-agent cookbook with two eval scripts. Questioned whether the description needs updating or the wrong files were replaced.
- **Fix:** PR description was updated during the session to reflect the new research-agent scope.
