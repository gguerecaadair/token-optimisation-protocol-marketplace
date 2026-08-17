# Token Optimisation Protocol — model routing

Opus triages every request and routes each sub-task to the cheapest tier that still does it excellently — **starting with "does this need a model at all?"** Deterministic work goes to plain code; the heavy thinking goes to the strongest models at full depth; the routine parts go to fast, economical ones.

| Sub-task | Tier |
|---|---|
| Deterministic — collection, parsing, merge, counting, dedup, tests | **plain code, no model** (0 tokens) |
| Read-only discovery, find/trace across files | Sonnet 5 (low) — scout |
| Tables, formatting, simple Q&A, routine edits, tests | Sonnet 5 (medium) — worker |
| Triage, synthesis, hard/correctness-sensitive code | Opus 5 (xhigh) — hub · heavy-worker |
| Plans, architecture, adversarial & methodology review, complex synthesis | Fable (xhigh) — planner |
| Verification of important work | Opus / Fable (xhigh) — reviewer |

Bundled: the five agents above and a `routing` skill carrying the triage policy (tier-zero-first, verify-by-reading, checkpoint-long-runs, verbatim-request briefs, EVIDENCE/ESCALATE contracts). Set once per person after install: default `model: opus` + `effortLevel: xhigh` (and, optionally, the cost meter). See the marketplace README for install/setup, `docs/for-colleagues.md` for a plain-English guide, `docs/how-it-works.md` for the full technical explainer, and `docs/worked-example.md` for measured token results from a real run.
