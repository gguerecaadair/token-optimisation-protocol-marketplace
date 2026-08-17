---
name: routing
description: Model-routing policy for Token Optimisation Protocol. Use at the start of a task to triage it — decide how to split the work and which tier does each part. First ask if a sub-task is deterministic (do it in plain code, no model, zero tokens); then simple → Sonnet, complex → Fable/Opus.
---

# Token Optimisation Protocol — route the work, not just the model

The **Opus** hub triages every request: break it into sub-tasks, and for each pick the cheapest thing that still does it *excellently* — starting with "does this need a model at all?" Quality drives; cost is saved by not over-spending on the easy parts, never by under-serving the hard parts.

## Who does what
| Sub-task | Tier |
|---|---|
| Deterministic work — collection, parsing, merge, counting, dedup, format conversion, tests | **Plain code, no model (tier zero — 0 tokens)** |
| Read-only discovery, find/trace across files, summarising docs | **Sonnet 5** (low) — scout |
| Tables, formatting, simple Q&A, routine edits, straightforward code | **Sonnet 5** (medium) — worker |
| Triage, synthesis, hard/correctness-sensitive code | **Opus 5** — hub · heavy-worker |
| Plans, architecture, adversarial & methodology review, complex synthesis, hard decisions | **Fable** — planner |
| Verification before ship | **Opus 5** / **Fable** (high-stakes) — reviewer |

*(Haiku isn't in the default ladder: the truly mechanical work is tier zero, and discovery needs Sonnet's relevance judgement rather than the weakest model on the job that feeds every downstream plan. Reach for Haiku only via an explicit `model: haiku` override for very high-volume, low-stakes bulk triage.)*

## Triage rules
1. **Tier zero first.** Before assigning any model, ask if the sub-task is deterministic (top row). If so, write and run code — zero tokens. Reach for a model only when the work needs judgement or generation. Usually the biggest single saving, especially for anything that recurs.
2. **Then: simple → cheap** (Sonnet); **complex → high quality** (Fable; hard code → Opus). When unsure **on a judgement-hard sub-task**, escalate — a wasted premium call beats a shallow result shipped.
2b. **Don't over-delegate** (recent Opus models delegate more readily, and spokes cold-read at full rate — every spawn has a fixed cost floor). Do it inline if a handful of tool calls finishes it, or the files are already in context. **Never delegate verification of a spoke's own work.** Cap parallel spawns at ~4 unless the fan-out is genuinely independent.
2c. **Write tight.** Recent models run longer by default and effort does not reliably shorten output — ask for length explicitly. No filler sections, redundant summaries or boilerplate.
3. **Verify by reading, don't re-derive.** Where ground truth is already in files, check claims by reading them — don't spend an agent to re-compute what you can read.
4. **Checkpoint long runs.** Write each sub-result to disk as it returns and skip completed steps on resume — never let an interruption re-run finished work.
5. **Pin the model on every delegation.** A `CLAUDE_CODE_SUBAGENT_MODEL` env var, if ever set, silently overrides all pins and flattens every tier onto one model — keep it unset.
6. **Every brief quotes the user's actual request verbatim in a QUOTE block.** Spokes see only what you pass them.
7. **Scout first, then hand the summary up — but the summary is a map, not ground truth.** The planner/worker re-reads the load-bearing files itself.
8. **A spoke return missing its EVIDENCE / COVERAGE / UNVERIFIED sections is a failed delegation.** Honour an `ESCALATE:` return by moving that sub-task up a tier.

## Deliverables
For customer-facing or report-shaped output, draft and assemble on one tier (fragments from different isolated spokes drift in voice and rule-adherence), inline your team's editorial standards into the brief, and hand the reviewer the rubric + source-of-truth files, not just the draft.

## Note on subagent context
Subagents auto-load the CLAUDE.md hierarchy, a git snapshot, and any skills named in their definition — but not the conversation or the hub's memory. Put standing rules in CLAUDE.md (they reach every spoke); pass task facts in the brief. Keep CLAUDE.md lean — it's re-read into every non-fork subagent on every spawn.

See `docs/worked-example.md` for measured token results from a real run.
