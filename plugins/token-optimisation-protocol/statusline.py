#!/usr/bin/env python3
"""Claude Code status line: model | dir | session cost | lines changed | duration.

Reads the status JSON on stdin and prints a single line. Every field is
optional and guarded, so it degrades to a blank line rather than erroring if
the harness sends a different schema. Copy to ~/.claude/ and wire it up via the
`statusLine` key in settings.json (plugins can't set statusLine themselves).
"""
import sys
import os
import json


def main() -> None:
    # Windows consoles default to cp1252, which can't encode the glyphs below.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    try:
        data = json.load(sys.stdin)
    except Exception:
        print("")
        return

    parts = []

    model = (data.get("model") or {})
    name = model.get("display_name") or model.get("id")
    if name:
        parts.append(f"\x1b[1;36m⬡ {name}\x1b[0m")  # bold cyan

    ws = data.get("workspace") or {}
    cwd = ws.get("current_dir") or data.get("cwd") or ""
    if cwd:
        base = os.path.basename(cwd.rstrip("/\\")) or cwd
        parts.append(f"\x1b[2m{base}\x1b[0m")

    cost = data.get("cost") or {}

    usd = cost.get("total_cost_usd")
    if isinstance(usd, (int, float)):
        parts.append(f"\x1b[33m${usd:.4f}\x1b[0m")  # yellow

    add = cost.get("total_lines_added")
    rem = cost.get("total_lines_removed")
    if isinstance(add, int) or isinstance(rem, int):
        parts.append(f"\x1b[2m+{add or 0}/-{rem or 0}\x1b[0m")

    dur = cost.get("total_duration_ms")
    if isinstance(dur, (int, float)) and dur > 0:
        mins = int(dur // 60000)
        secs = int((dur % 60000) // 1000)
        parts.append(f"\x1b[2m{mins}m{secs:02d}s\x1b[0m" if mins else f"\x1b[2m{secs}s\x1b[0m")

    print(" \x1b[2m·\x1b[0m ".join(parts))


if __name__ == "__main__":
    main()
