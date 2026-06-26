# Security & privacy — Ainvis Local

Ainvis Local runs entirely on your own machine. This document explains what it does, what it touches, and — importantly — what it does **not**.

## Data & network

- **Local-first.** Everything — conversations, minutes (`minutes/`), decisions (`decisions.md`) and your own reference files (`library/`) — is stored as plain Markdown in your workspace folder. Uninstalling never deletes it.
- **No telemetry.** Ainvis Local sends nothing to XPAND or to any server of ours.
- **The only LLM traffic is yours.** The executives run inside your own Claude Code, on your own Claude subscription (or API key). We are not in that path.

## The boardroom viewer is NOT connected to Claude

The bundled viewer (`/ainvis-local:viewer`) is a **read-only local renderer**, not an AI client:

- It is a Python **standard-library** HTTP server bound to **`127.0.0.1`** (localhost only — it is not exposed to your network).
- It serves a static page plus your meeting's local Markdown log.
- It **never connects to Claude / Anthropic, never reads or uses your Claude credentials, and makes no Anthropic API calls.**
- The flow is strictly **one-way**: Claude Code writes the meeting log; the viewer only displays it.
- Its only outbound request is loading XPAND's self-hosted brand fonts from our CDN, with a graceful system-font fallback when offline.

Because the viewer never sends prompts to Claude, it raises no terms-of-use concern — it is not a third-party app driving your Claude subscription.

## Hooks — what runs automatically

| Hook | Event | What it does |
|---|---|---|
| `hooks/meeting_auto_approve.py` | PreToolUse | Auto-approves **only** (a) reads/writes whose destination is inside an Ainvis Local workspace (a folder tree containing `decisions.md`) and (b) launches of the five bundled persona subagents. Excludes any `/.git/` or `/.claude/` path. **Fails open** — it never blocks the normal Claude Code permission flow. |
| `hooks/meeting_timestamp.py` | PostToolUse | After the meeting log is written, fills empty per-turn timestamps from the local clock (minute precision). No shell execution. |
| `hooks/load_context.py` | SessionStart | Reads `decisions.md` (read-only) so the board carries continuity between sessions. Prints nothing outside an Ainvis Local workspace. |

The auto-approval exists so a board meeting doesn't prompt you on every single turn. It is bounded to your meeting files and the five personas; everything else defers to Claude Code's normal permission prompts. All three hooks are plain Python you can read in `hooks/`.

## Dependencies

- The viewer needs **Python** (standard library only — no third-party packages).
- **No fonts or binaries are bundled or redistributed.** Fonts are served from a CDN with a system-font fallback.

## Reporting a vulnerability

Please report security issues privately via this repository's **GitHub Security Advisories** (the *Security* tab → *Report a vulnerability*), or contact XPAND K.K. via https://xpand.co.jp. Please do not open a public issue for a security report.
