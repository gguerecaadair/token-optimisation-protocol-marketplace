# How it works — technical explainer

A developer-facing account of the Token Optimisation Protocol routing: what it is, the mechanism, and the sharp edges. Accurate to current Claude Code docs; version-gated behaviour is flagged.

## Model
Hub-and-spoke over Claude Code subagents. One **orchestrator** (main loop, Opus 5) + five subagents in `agents/*.md` (frontmatter: `name`, `description`, `tools`, `model`, `effort`; body = system prompt) — plus a **tier zero that isn't a model at all**. Each non-fork subagent runs in its own context window.

## The core idea: route the *work*, not just the model
The hub triages each request and, for every sub-task, picks the cheapest thing that still does it excellently — **starting with "does this need a model?"** Deterministic work (collection, parsing, merges, counting, dedup, format conversion, tests) is done in plain code at **zero tokens**. Only judgement or generation reaches a model.

| Sub-task | Tier |
|---|---|
| Deterministic (collection, parse, merge, count, dedup, tests) | **plain code — no model, 0 tokens** |
| Read-only discovery, find/trace across files, summarising docs | Sonnet 5 (low) — scout |
| Tables, routine edits, straightforward code, tests | Sonnet 5 (medium) — worker |
| Triage, synthesis, hard/correctness-sensitive code | Opus 5 — hub · heavy-worker |
| Plans, architecture, adversarial/methodology review | Fable — planner |
| Verification before ship | Opus (Fable high-stakes) — reviewer |

**Haiku is deliberately not in the default ladder.** The truly mechanical work is tier zero (free), and discovery needs relevance judgement — putting the weakest model on the map that every downstream plan trusts is a confidence-laundering risk. Reach for Haiku only via an explicit `model: haiku` override, for very high-volume, low-stakes bulk triage on a bounded corpus.

## How routing actually happens
No router model or classifier — it's emergent from the orchestrator's tool-use reasoning. Claude Code surfaces the agent roster (`name` + `description`) as `subagent_type`s on the **Agent** tool (renamed from `Task` in v2.1.63; `Task` still aliases). The hub matches task → agent by description plus the triage policy in its context, and emits an Agent call with an optional per-invocation **`model`** override. **Effort has no per-invocation override** — it is frontmatter or session-inherited only. Per-tier reasoning depth = adaptive thinking bounded by that agent's effort (subagents inherit the main conversation's thinking on/off as of v2.1.198).

## Resolution precedence (top wins)
**Model:** `CLAUDE_CODE_SUBAGENT_MODEL` env (overrides everything and silently flattens all subagents onto one model — keep it unset) → per-invocation `model` → frontmatter `model` → main model. Each candidate is checked against the org `availableModels` allowlist; an excluded value is **silently** skipped and the inherited model runs (no error). `=inherit` equals "unset" as of v2.1.196.
**Effort:** `CLAUDE_CODE_EFFORT_LEVEL` env (overrides *including* frontmatter) → frontmatter (overrides session) → session → model default. Frontmatter-over-session is why the hub runs `xhigh` while scout stays `low` and worker `medium`.

## What a subagent receives at startup
A non-fork subagent's context = its system prompt + the brief + **the full CLAUDE.md hierarchy** + a **git-status snapshot** + skills **named in its `skills` frontmatter** + (v2.1.206+) the **sibling roster**. It does **not** see the parent conversation, auto-memory, already-invoked skills, or files already read. (Built-in Explore/Plan skip CLAUDE.md + git; a **fork** subagent inherits the whole parent conversation.) **Consequence:** CLAUDE.md is cold-read into every non-fork spawn — a per-dispatch token cost, so keep it lean; standing rules there reach every spoke automatically, task-specific facts go in the brief.

## Reliability contracts
- **Verbatim-request QUOTE block** in every brief; the reviewer diffs acceptance criteria from it *before* reading code — a brief without it is a finding (otherwise it validates the hub's paraphrase against itself).
- **Scout is search-and-discard:** verbatim `file:line`, the exact greps behind any absence claim; downstream agents re-read load-bearing files (the summary is a map, not ground truth).
- Every spoke returns **`EVIDENCE / COVERAGE / UNVERIFIED`** (missing = failed delegation); cheaper tiers return **`ESCALATE:`** on subtle work (auth, concurrency, money maths) rather than satisfice.
- **Checkpoint-and-resume:** each result written to disk on return; an interruption never re-runs finished work.
- **Verify by reading, not re-deriving:** check against files where ground truth already exists.

## Cost / performance (read before assuming it saves money)
Delegation is **context-protection and parallelism, not a cost win by default.** Subagents don't share the hub's prompt cache: the hub re-reads its own context at cache-read (~0.1× input) rates, while a spoke **cold-reads** the same material at full rate. For a mid-size task whose files are already warm in the hub, a single-model loop can be cheaper than delegating. Delegation pays off for large discardable reads, bulk low-cost output, and genuine parallelism. Pricing per 1M in-out: Fable $10/$50, Opus $5/$25, Sonnet $2/$10 intro → $3/$15 (after 31 Aug 2026), Haiku $1/$5.

## Observability & enforcement (honest state)
A model self-tag on the reply (e.g. `[planner · Fable]`) is a cheap signal but **can lie** — an `availableModels` exclusion silently runs the inherited model, and **no hook exposes the resolved model** (`SubagentStart`/`SubagentStop` carry only `agent_id`/`agent_type`). Ground truth: **`/usage`** per session; **OTel** telemetry (`claude_code.cost.usage` / `token.usage` carry `model` *and* `effort` attributes) for cross-session — needs a collector. Routing is **advisory**, not enforced; a `PreToolUse` hook on `Agent` can deny-with-reason, but the hook's visibility into `subagent_type`/brief/model is **undocumented** — validate empirically before relying on it.

## Measured result
A real multi-stage run: ~497K delegated tokens, ~two-thirds below the top tier — extraction 223K (Sonnet), verification 164K (Opus), design 110K (Fable), collection + merge + tests 0 (plain code). Full numbers, measured vs estimated, in [`worked-example.md`](./worked-example.md).

## Version dependence
Resolution behaviour moved across v2.1.196 (`inherit` semantics), .198 (subagent thinking inheritance; Explore inherits the main model; background-by-default), .206 (sibling roster), .211 (per-invocation model on resume). Pin `autoUpdatesChannel: "stable"` and re-verify per-agent model/effort after upgrades; check your installed version if behaviour differs from the above.
