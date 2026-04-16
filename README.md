# 🍧 GL AIP (GDP Labs AI Agent Package) Cookbook

Welcome to the **GL AIP Cookbook** - a comprehensive collection of sample code and examples for working with the GL AIP SDK.

## Quick Start

1. Install Python 3.11 or 3.12
2. Install [uv](https://docs.astral.sh/uv/)
3. Pick an example under [`./examples`](./examples/) and follow that example's README

## Examples

- **Default server-backed flows**: `hello-world`, `multi-agent`, `runtime-config`, `modular-tool-integration`, `agent-export-import`
- **Local-run flows**: `hello-world-local`, `multi-agent-system-patterns`, `tool-state-handoff-local`

Each example README contains its own prerequisites and environment configuration.

---

## What Are Agent Skills?

Agent Skills let you **extract reusable instruction blocks** from your agent prompts and reference them by name instead of rewriting them everywhere.

**How it works:**

1. You write a **skill** (a small markdown file with policy/rules/templates)
2. Your agent instruction **references** that skill by name instead of writing the full text
3. At runtime, the agent fetches the skill content automatically

**Example:**

```
# Before (without skills)
You are a screening agent. 
If score >= 8, recommend PASS. If score < 8, recommend FAIL.
For PASS, update phase to 'hr_interview'.
For FAIL, update phase to 'disqualified' with reason 'Tidak memenuhi standar minimum'.

# After (with skills)
You are a screening agent. Follow skill "cv_scoring_policy" and "phase_update_contract".
```

The skill files contain the full policy text. The agent loads them at runtime.

---

## Should I Migrate This Instruction to Agent Skills? (Quick Heuristics)

### Signs it's a GOOD candidate ✅

| Heuristic | Why It Matters |
| :---- | :---- |
| **Instruction >100K tokens** | Enough content to extract meaningful skills |
| **Repeated policy blocks (3+ times)** | Skills eliminate duplication (see example below) |
| **Shared across multiple agents** | One skill serves many → multiplicative savings |
| **Large if/else branches** | Can become skill references - cleaner orchestration |
| **Reusable output schemas or templates** | Same JSON structure or email template appears multiple times → extract to skill |

**What "repeated policy blocks" means (example):**

In a screening agent instruction, you might see the same policy written 3+ times:

```
1. "If score >= 8, recommend PASS. If score < 8, recommend FAIL."
2. "For PASS candidates, update phase to 'hr_interview'."
3. "For FAIL candidates, update phase to 'disqualified' with reason 'Tidak memenuhi standar minimum'."
```

This logic appears in multiple places (scoring, phase update, output). Extract it to a skill → saves tokens every time the agent uses it.

Another example: email templates that appear verbatim in multiple sections of the instruction.

### Signs it's a BAD candidate ❌

| Heuristic | Evidence | Why It Matters |
| :---- | :---- | :---- |
| **Instruction <50K tokens** | (see Warning 2 below) | Skills add ~10-15K overhead, not worth it for small prompts |
| **Single-purpose, no repeats** | (see Warning 2 below) | Nothing meaningful to extract - skills add without removing |
| **Would become one giant skill** | (see Warning 2 below) | Mega-skill anti-pattern - hurts cost instead of helping |

### After Migration: Validate with Benchmark

Run baseline vs skills to confirm:

| Token Reduction | Decision |
| :---- | :---- |
| > 15% | ✅ Adopt |
| 10-15% | ⚠️ Adopt with caution |
| 0-10% | ❌ Rethink - marginal benefit |
| < 0% | ❌ Reject - cost increased |

---

## Data-Backed Results from Our Experiments

| Case | Token Change | Speed Change | Outcome |
| :---- | ----: | ----: | :---- |
| **Success 1** - Screening flow | **-29.63%** | +39.80% faster | ✅ Win |
| **Success 2** - Sub-agent migration | **-54.07%** | +67.81% faster | ✅ Win |
| **Success 3** - Generalized two-agent | **-36.35%** | +49.81% faster | ✅ Win |
| **Warning 1** - Speed worsens (same case as Success 2) | -54.07% | -67.81% slower | ⚠️ Check latency |
| **Warning 2** - Token cost worsens | **+30.50%** | +16.45% faster | ❌ Reject - instruction too small |

**Key insight**: Success cases had **100K+ tokens** with clear repeated blocks. Warning 2 (token cost worsens) had only **51K tokens** with no real repetition → skills added overhead instead of saving.

---

Explore the subdirectories in the [examples](./examples/) folder for hands-on code and setup instructions.