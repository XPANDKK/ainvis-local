#!/usr/bin/env python3
"""PostToolUse: stamp per-turn timestamps in live-meeting.md from Python's clock.

The meet skill rewrites the whole live log each turn (to avoid the Read-tool
mojibake on Windows) and leaves the per-turn timestamp field empty — the
orchestrator has no clock. This hook fills those empty timestamps with the local
time (minute precision; no shell, so no Yes prompt). A small sidecar keyed by
persona+body remembers each turn's first-seen time, so the whole-file rewrites
keep each turn's time stable instead of all jumping to "now". Runs AFTER the
write, so it never clashes with Claude Code's write-size verification, and it
reads/writes UTF-8 explicitly so it never mojibakes.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import datetime

_TURN_RE = re.compile(r"(::turn::[^\n]*)\n([\s\S]*?)\n::end::")


def _sidecar_path() -> pathlib.Path:
    pd = os.environ.get("CLAUDE_PLUGIN_DATA")
    base = pathlib.Path(pd) if pd else pathlib.Path.home() / ".ainvis-local"
    return base / "turn-times.json"


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError, OSError):
        sys.exit(0)

    tin = data.get("tool_input") or {}
    if not isinstance(tin, dict):
        sys.exit(0)
    fp = tin.get("file_path") or tin.get("path")
    if not fp or pathlib.Path(str(fp)).name != "live-meeting.md":
        sys.exit(0)

    path = pathlib.Path(str(fp))
    if not path.is_absolute():
        path = pathlib.Path(data.get("cwd") or ".") / path
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)

    sc_path = _sidecar_path()
    try:
        sidecar = json.loads(sc_path.read_text(encoding="utf-8")) if sc_path.exists() else {}
    except (OSError, ValueError):
        sidecar = {}
    if not isinstance(sidecar, dict):
        sidecar = {}

    # Local time, minute precision, offset-aware (e.g. 2026-06-25T10:50+09:00).
    now = datetime.now().astimezone().isoformat(timespec="minutes")
    state = {"changed": False}

    def repl(m: "re.Match[str]") -> str:
        header, body = m.group(1), m.group(2)
        parts = header.split("|")
        if len(parts) < 4:
            return m.group(0)
        if parts[3].strip():  # already stamped
            return m.group(0)
        pid = parts[0].replace("::turn::", "").strip()
        key = hashlib.sha1((pid + "\n" + body.strip()).encode("utf-8")).hexdigest()
        t = sidecar.get(key)
        if not t:
            t = now
            sidecar[key] = t
        parts[3] = " " + t
        state["changed"] = True
        return "|".join(parts).rstrip() + "\n" + body + "\n::end::"

    new_text = _TURN_RE.sub(repl, text)
    if state["changed"] and new_text != text:
        try:
            path.write_text(new_text, encoding="utf-8")
            sc_path.parent.mkdir(parents=True, exist_ok=True)
            sc_path.write_text(json.dumps(sidecar), encoding="utf-8")
        except OSError:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
