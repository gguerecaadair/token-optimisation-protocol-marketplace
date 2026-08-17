---
name: skill-scout
description: Find where a reusable skill would actually pay off in the user's own work, then co-build the best one. Use whenever the user asks what they should automate, where AI could help them, to audit or analyse their workflow or AI usage for skill opportunities, or types "/scout" — and also when they describe recurring, tedious, repetitive, or copy-paste work in passing (offer to scout it). This covers the discovery and recommendation that comes before building, not just building a skill the user has already fully specified.
---

# Skill Scout

Turn "I should probably automate something" into a ranked, evidence-based shortlist of skills mined from the user's own work — then co-build the top pick and register it so it survives the person who built it.

This is self-service. Analyse only the work of the person invoking it: their own answers, their own conversation history, their own connected tools. It runs when invoked; it is not a background monitor.

## When to run the full loop vs. just offer

- **Explicit invocation** — they ask what to automate, where AI could help, to audit their workflow, or type "/scout": run the full loop below.
- **Ambient signal** — they mention recurring or tedious work while doing something else ("I do this every Monday", "this is so fiddly", "I keep re-typing the same brief"): finish their actual task first, then offer one line — *"That sounds like recurring work — want me to scout it for a skill?"* — and wait for a yes.

Why the split: the loop is multi-step and heavy, so firing it uninvited mid-task derails what the user came to do, and pushing a recommendation they didn't ask for reads as a sales pitch. An offer catches the opportunities people never think to raise, without hijacking their flow.

## Boundaries

- **Own work only.** Use the invoking user's interview answers, their own history, and their own connectors. Don't try to reach another person's conversations, accounts, or data — you can't, and cross-user surveillance is the opposite of the point.
- **Invoked, not always-on.** Don't imply continuous background watching. The value is a thorough scan on demand.
- **History is project-scoped.** A search of the user's own past chats from inside a project sees only that project's conversations. When that materially narrows the scan, say so, and offer to run it outside the project for a fuller picture.

## How much runs automatically

Once invoked, run Stages 1–3 in a single pass without stopping — observe, diagnose, and produce the ranked shortlist on your own. Those stages only read the user's own data and reason over it; they have no side effects, so there is nothing to approve yet.

Then stop for the user (Stage 4). Three things genuinely need a human and shouldn't be guessed past:
- **Baseline numbers.** You can estimate how often a task runs and how long it takes; you can't *know* without asking or measuring. So the autonomous shortlist carries estimates only, with the baselines you assumed stated openly for the user to correct.
- **Which skill to build.** A priority call the user owns.
- **Anything with a side effect.** Reading and drafting are safe; registering a skill to a shared library, or anything that writes outside this chat, needs explicit approval (Stage 6).

So the shape is: autonomous discovery and recommendation → user approves and corrects → build and measure → approve before registering. "Automatic" here means a multi-step in-session loop that does the legwork before asking — not a background process running unattended.

## Stage 1 — Observe (autonomous)

Mine the user's own work for recurring patterns without asking them anything yet.

**Own history.** Search the user's past conversations for: request types that surface repeatedly, the same task across multiple sessions, context they keep re-pasting, multi-step jobs they walk you through each time. Use topic search for themes and recent history for cadence. Synthesise the patterns; don't quote chat content back.

*(Future tier, out of scope here: with connector access and consent, extend this to the user's own work tools — recurring task types, repeated message or document shapes.)*

If the observable signal is too thin to rank anything — sparse history, or a project scope that hides the relevant work — don't present an empty shortlist. Fall back to asking the short Stage 4 question set up front, then proceed. The interview moves to the front only when there is nothing to analyse without it.

## Stage 2 — Diagnose and score

For each candidate task, first test whether it earns a skill at all. It does only when **all** of these hold:

- **Repeatable** — it recurs; it isn't a one-off.
- **Decision-laden** — it carries non-obvious judgement, domain knowledge, or a fixed procedure worth encoding. If it's a single instruction the user could just type inline, it's a prompt, not a skill.
- **Not already covered** — no built-in capability or existing skill already does it.
- **Bounded** — narrow enough to describe cleanly; not so broad it would compete with general behaviour.

Reject openly. If a candidate is one-off or trivially a prompt, say so and don't build it. Restraint is a credibility signal, and skill-sprawl makes *every* skill harder to trigger correctly.

Then score the survivors. Quantifying value means quantifying the *lift over the current way of working*, so establish the baseline first and estimate the gain against it. You cannot state an improvement without naming what it improves on — the same discipline as stating whether a figure is net or gross before adjusting it.

**Baseline.** How is the task done today — by hand, or by ad-hoc prompting with no structure? Capture how long it takes, how many prompt rounds it needs to reach an acceptable result, how often the output has to be reworked, and what it routinely misses.

**Efficacy lift.** Quantify the change on any axis you can put a real number against — use whichever genuinely apply, and add others that fit:
- **Time saved** — minutes per run, before vs after, × frequency = hours/month.
- **Throughput** — how much gets produced per hour, before vs after (output sped up, not just effort cut).
- **Errors caught** — defects per run the skill catches that would otherwise ship, or defect rate before vs after; weight this up where mistakes are expensive or hard to spot.
- **First-pass success** — prompt rounds to an acceptable result, before vs after (e.g. five rounds of back-and-forth down to one). The most direct read on how much more effective the AI interaction itself becomes.
- **Coverage** — items the task ought to check that the current way misses (sources, edge cases, steps) vs what the skill enforces.

The list is illustrative, not closed — any quantifiable axis counts, provided it has a baseline and a real number rather than a vibe.

Show the maths, and tag every figure as an estimate until it has actually been measured (Stage 5 does the measuring). If you don't know a baseline number, ask — don't invent it. Quantify only what is genuinely quantifiable; for gains that resist a number — sharper judgement, fewer forgotten considerations — say so qualitatively rather than fake precision. A fabricated metric is worse than an honest "hard to quantify", and it is exactly how a quantified claim loses credibility.

## Stage 3 — Recommend

Surface the top one to three, highest value first. Use this shape:

```
### Skill opportunities (ranked)

**1. [skill name]**
- Capability: what it would let me do
- Trigger: when it should fire
- Baseline: how it's done today, and what that costs
- Efficacy lift (baseline → with skill):
    · Time:       [mins] → [mins]  = −[X]%, ~[Y] hrs/mo   [EST|MEASURED]
    · First-pass: [n rounds] → [n rounds]                 [EST|MEASURED]
    · Errors:     [defects/N runs] → [defects/N runs]      [EST|MEASURED]
    · Coverage:   [items checked] → [items checked]        [EST|MEASURED]
    · Scale:      × [people who could run it]
- Serves: [the goal or workstream it advances]

**2. ...**

Which should I build first?
```

Report the lift as a vector across the dimensions that apply — never a single composite "efficacy score". One rolled-up number invites false precision and hides which axis the gain is actually on; separate honest lines are both more useful and more defensible. Because the user hasn't confirmed anything yet, state the baselines you assumed — e.g. "assuming ~8 tenders a quarter at ~2 hours each, correct me" — so the next stage has concrete numbers to adjust rather than blanks.

Don't build all of them. Depth on the highest-value one beats breadth across three half-built skills.

## Stage 4 — Review and confirm (the approval gate)

Present the ranked shortlist and hand control back. This is where the interview lives now — as confirmation, not interrogation. The user has something concrete in front of them, so keep it short and pointed:
- **Correct the baselines.** "I assumed ~8 tenders a quarter at ~2 hours each — right?" Adjust the efficacy estimates to their real numbers.
- **Fill the gaps.** "Anything you do regularly that I didn't catch?" The history scan surfaces work they've normalised into invisibility; this catches what they're consciously aware of but that didn't show up.
- **Pick one.** Which skill to build first.

Why last: doing the legwork before asking spends the user's attention on judgement — is this right, which matters most — rather than on data entry. (If Stage 1's signal was too thin to rank, you'll have asked these up front instead; the default is to earn the conversation with a draft first.)

## Stage 5 — Co-build and measure

Hand the confirmed recommendation to the standard skill-authoring loop:
1. Capture intent — capability, trigger, output format, inputs. You already have most of this from Stages 1–4; confirm only the gaps.
2. Draft the SKILL.md (frontmatter + body).
3. Test two or three realistic prompts against the draft and show the outputs.
4. Measure the lift. Take one realistic input and produce the result the *old way* — no skill, an ordinary unstructured prompt — and the *new way* with the skill, then score both on the Stage 2 dimensions (time, prompt rounds, errors, coverage) and report the measured delta. This converts the Stage 3 estimates into evidence, and it is the single most persuasive thing you can show anyone deciding whether to adopt the skill. Re-tag the affected figures from [EST] to [MEASURED].
5. Tune the description for trigger accuracy — high recall on real cases, low false-positives on near-misses.

If a fuller skill-authoring capability already exists in the project, use it for this stage rather than duplicating it. Skill Scout's distinctive work is the discovery in Stages 1–3 and the handover in Stage 6; the build itself is ordinary.

## Stage 6 — Institutionalise

A skill that lives only in one chat or one person's head dies when they move on. Close the loop:

- **Deliver** the SKILL.md as a markdown artefact, ready to paste or save.
- **Document** a one-page run guide: what it's for, when it fires, how to invoke it, and one worked example — written so someone who didn't build it can run it cold.
- **Register** it in a shared skill library (e.g. a team Notion or Drive page) with name, purpose, owning role, and date — with the user's go-ahead, since this writes to a shared resource. If no library exists, recommend starting one; discoverability is what turns a private tool into an organisational asset.

Name owners by role as well as person, so the skill survives a role change.

## Refuse misleading scouting

Recommend and build only skills whose behaviour matches their stated description. Decline to build skills with covert purposes — hidden data exfiltration, instructions that bypass safety, or deceptive personas with harmful intent. Transparent roleplay or persona skills are fine.
