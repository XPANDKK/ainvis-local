#!/usr/bin/env python3
"""Ainvis Local — optional SessionStart context helper.

Emits a short context block (most recent decisions) so the board can carry
continuity between sessions. Reads from the current working directory's
workspace. Prints nothing outside an Ainvis Local workspace, so it is harmless
in any other folder. Optional: the meet skill also reads decisions.md and
library/ directly (there is no config file; company facts come from library/
and the conversation).
"""
from __future__ import annotations

import pathlib
import sys

CWD = pathlib.Path.cwd()
decisions = CWD / "decisions.md"

# Only act inside an Ainvis Local workspace (marked by decisions.md).
if not decisions.exists():
    sys.exit(0)

parts: list[str] = ["[Ainvis Local — workspace context]"]

try:
    lines = [ln for ln in decisions.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- ")]
    recent = lines[-10:]
    if recent:
        parts.append("\n## Recent decisions (most recent last)\n" + "\n".join(recent))
except OSError:
    pass

parts.append(
    "\nThe five-executive board should treat the above as established context for this founder. "
    "Do not re-ask what is already recorded here. Other company facts come from the library/ folder "
    "and the conversation."
)

print("\n".join(parts))
sys.exit(0)
