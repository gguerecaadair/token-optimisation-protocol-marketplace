# Worked example — measured token efficiency

A real multi-stage task run through this plugin's routing: a competitive-intelligence build (multi-source document ingest → verified spec dataset → report). The figures in §2 are **measured / exact**; §3 are **estimates with stated assumptions**, not measurements.

## 1. The disciplines that compounded
- **Route the work, not just the model.** Deterministic steps — source collection, the data merge, tests — ran as plain code at **zero tokens**, not as LLM agents.
- **Context isolation.** Each heavy read ran in its own isolated subagent, so large source documents never piled into the main conversation to be re-processed on every later step.
- **Checkpoint-and-resume.** Each result was written to disk the instant it returned, so an interruption never re-ran finished work.
- **Verify by reading.** Where ground truth already sat in files, claims were checked by reading them — not by spending an agent to re-derive them.

## 2. What each tier did — measured (exact)
| Stage | Tier | Tokens |
|---|---|---|
| Source collection | plain code — no model | **0** |
| Data merge + grounding + gate tests | plain code — no model | **0** |
| Document extraction (bulk, careful reading) | Sonnet 5 | **223,000** |
| Adversarial verification (the correctness gate) | Opus 4.8 | **164,000** |
| Architecture design (hardest reasoning, used once) | Fable | **110,000** |
| Triage, synthesis, writing | Opus 4.8 (hub) | main thread |
| **Total delegated (measured)** | mixed | **~497,000** |

The two most token-heavy jobs (extraction 223K, design 110K) ran on the *cheaper* tiers; the verification — where being wrong is expensive — got the premium tier. **Roughly two-thirds of the measured delegated tokens ran below the top tier.**

## 3. What it would have cost without the approach — estimated
- **Naive path** (one premium model, one shared context that carries every prior document forward): plausibly **~2–3× the tokens** one-off, and it draws the usage budget several× faster again (premium tiers cost roughly 5×+ per token vs Sonnet).
- **Recurring:** a free code-based collector avoids an estimated **~0.3–0.8M tokens per week** (≈15–40M/year) versus an LLM fan-out of collector agents — the single largest, recurring saving.
- **Resume risk:** one prior failed resume that invalidated its cache cost ~**1.28M tokens** — the case for checkpoint-and-resume.

## 4. One line
> Premium models on judgement and correctness; the cheap model and plain code on bulk reading and deterministic work. Under ~0.5M measured tokens instead of an estimated 2–3× that, plus a recurring weekly saving from making collection free.
