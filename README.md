# VSE EDU BM — Claude Code plugins

A Claude Code plugin marketplace. Currently ships one plugin: **Efficient Excellence** — Opus-triaged model routing.

## Install

From an interactive `claude` session (or the desktop app):

```
/plugin marketplace add gguerecaadair/efficient-excellence-marketplace
/plugin install efficient-excellence@vse-edu-bm-plugins
```

- Swap the first line for a local path if you have the folder synced, e.g. `/plugin marketplace add "C:\path\to\efficient-excellence-marketplace"`.
- CLI equivalents: `claude plugin marketplace add ...` then `claude plugin install efficient-excellence@vse-edu-bm-plugins`.
- If `claude plugin ...` reports a git "unsafe location" error, run it from `C:\` rather than your home directory.

Installing bundles the five routing agents (scout, worker, heavy-worker, planner, reviewer) and the `routing` skill.

## Two things to set once (plugins can't set these for you)

1. **Default model + effort** — in your `~/.claude/settings.json`:
   ```json
   { "model": "opus", "effortLevel": "xhigh" }
   ```
   This makes the Opus hub run at full reasoning depth. Agent-level effort overrides it, so the cheap tiers stay economical.

2. **(Optional) Cost meter** — copy `plugins/efficient-excellence/statusline.py` to `~/.claude/statusline.py`, then add to `settings.json`:
   ```json
   { "statusLine": { "type": "command", "command": "python C:\\Users\\<you>\\.claude\\statusline.py" } }
   ```

3. **(Optional) Always-on policy** — the routing behaviour comes from the agents automatically. To make the full triage posture always-on, paste the contents of the `routing` skill into your `~/.claude/CLAUDE.md`; otherwise invoke it per task with `/efficient-excellence:routing`.

## What bundles vs. what you set

| Bundled by the plugin | Set once per person |
|---|---|
| The 5 routing agents | Default `model` + `effortLevel` |
| The `routing` skill (triage policy) | Cost meter (`statusLine`) — optional |
| — | Always-on policy in `CLAUDE.md` — optional |

## Notes

- **Check the tiers actually took.** If a model isn't available on your plan or org allowlist, Claude Code **silently** runs your main model instead — no error, and the routing quietly collapses to one tier. After your first run, check `/usage` to confirm more than one model appears.

- Claude Code only (not claude.ai). Config is per-machine.
- Start a **new chat** after installing for it to take effect.
