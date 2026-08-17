# Token Optimisation Protocol — a plain-English guide

For colleagues who use AI every day but don't write code. No jargon — just what it does, how it works, and why it's cheaper.

## What it is
A Claude Code plugin that automatically uses the *right* AI model for each part of a job. The strongest models (which are also the slowest and priciest) handle the hard thinking; fast, cheap models handle the simple bits; and anything purely mechanical is done by plain code — no AI, no cost. You get top-quality results without paying top-tier price, or waiting, for the routine parts.

## How to install and use
1. Open **Claude Code** and paste these two lines. (Opening the repo link in a browser doesn't install it — these commands do.)
   ```
   /plugin marketplace add gguerecaadair/efficient-excellence-marketplace
   /plugin install token-optimisation-protocol@vse-edu-bm-plugins
   ```
2. Set your main model to **Opus** — type `/model` and pick Opus. This is the "coordinator" that routes everything.
3. **Start a fresh chat.** That's it — it runs automatically, with nothing to switch on per task.

*Optional, for maximum quality every session:* add `"model": "opus", "effortLevel": "xhigh"` to your `~/.claude/settings.json` — or just ask Claude Code to do it for you.

## How it works
Think of it as a smart team lead with a team of different specialists.

Every request goes first to a **coordinator** (the Opus model). It reads what you've asked, splits it into smaller jobs, and hands each job to whoever is best suited — never using an expensive specialist for something a cheaper one does just as well. Four things make that work:

1. **The right model per job.**
   - *Mechanical work* — collecting data, merging files, counting, running checks → done as **plain code, no AI**.
   - *Quick, simple work* — lookups, tables, tidy-ups, reading across files → a **fast, cheap model** (Sonnet).
   - *Hard thinking* — planning, tricky problems, and checking important work before it goes out → the **most capable models, at full depth** (Opus and Fable).
2. **Mechanical work is done by code, not AI.** If a task is just following rules — gather these files, merge them, count the results — a small script does it instantly and for free. No AI tokens spent at all.
3. **Big reading is done in side tasks, then set aside.** When a job needs a large document read, that happens in a separate "helper" so the big document doesn't pile up in the main conversation. This matters because of how AI billing works (next section).
4. **It saves its progress.** Long jobs write each result to disk as they finish, so if something is interrupted it picks up where it left off instead of redoing hours of finished work.

You don't choose any of this — the coordinator does it for you.

## Why it's efficient (the token optimisation, in plain terms)
AI is billed by the "token" (about half a word), for everything the model reads *and* writes. Two facts drive the whole design:

- **The best models cost several times more per token.** The top tier is roughly 5–10× the price of the cheap one. So the trick isn't "use less AI" — it's *don't spend the expensive models on easy work.* Point them at the hard 20%; let the cheap model and plain code carry the rest.
- **A conversation re-reads its whole history on every step — and you're billed for it each time.** So if a huge document sits in the main conversation, you pay to re-read it again and again as the task goes on. By reading big documents in isolated side tasks and only bringing back a short summary, the main conversation stays light — and the bill stays small.

Add the free mechanical work (point 2) and the save-your-progress habit (point 4), and the savings compound.

**What that looked like on a real job** (a multi-step competitive-intelligence build):
- It came in **under ~0.5 million tokens**, with about **two-thirds of that handled below the top tier** (the cheap model and plain code did the bulk; the expensive models only did the hard reasoning and the final correctness check). *(These are measured figures.)*
- Doing the same job the naive way — one powerful model doing everything in one ever-growing conversation — would have cost an estimated **2–3× more**.
- And because the weekly data-collection step is a free script rather than AI, it avoids an estimated **0.3–0.8 million tokens every week** — a saving that repeats for as long as the tool runs. *(These two are estimates, with assumptions; the exact breakdown is in `worked-example.md`.)*

The short version: **premium models on judgement and correctness; the cheap model and plain code on everything else.**

## One handy lever
For a job that deserves the absolute best effort, type **`ultracode`** in your message — that turns everything up to maximum for that one task.

## How you'll know it's working
A small readout at the bottom of Claude Code shows the running cost of the session, and the AI tells you which model handled each hard step.
