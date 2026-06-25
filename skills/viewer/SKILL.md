---
name: viewer
description: Start the Ainvis Local boardroom viewer — a local web page that shows the five executives discussing in real time. Open it next to Claude Code before or during a board meeting.
---

# Ainvis Local — Boardroom viewer

Start the local viewer server and open the boardroom page. The viewer reads `meetings/live-meeting.md` in the current workspace and renders each executive's turn as it is written.

## Steps

1. **Confirm a workspace exists — you do NOT need to be in it, and you must NOT ask the founder to `cd`.** The server follows the active meeting through the `${CLAUDE_PLUGIN_DATA}/active.json` pointer that `meet` writes, so it shows the live boardroom from any directory. Just check a workspace exists somewhere: the current directory has `decisions.md`, or `./ainvis-local-workspace/decisions.md` exists, or the `${CLAUDE_PLUGIN_DATA}/workspace.json` pointer (fallback `~/.ainvis-local/workspace.json`) names a folder with `decisions.md`. If at least one exists, proceed (start the server from wherever you are). Only if none exists anywhere, tell the founder to run `/ainvis-local:setup` first and stop.
2. Confirm Python is available (`python --version` or `python3 --version`). The viewer needs it (always-on-top window + self-hosted Futura). If it is missing, do NOT fail — point the founder to `/ainvis-local:doctor`, which installs Python for them, then come back here.
3. Start the viewer server in the background, from the workspace directory, using the plugin's bundled script:
   ```
   python "${CLAUDE_PLUGIN_ROOT}/viewer/serve.py"
   ```
   (If `${CLAUDE_PLUGIN_ROOT}` is not expanded in your environment, use the path where the `ainvis-local` plugin is installed, e.g. `python <plugin-dir>/viewer/serve.py`.)
4. Tell the founder the viewer is at **http://127.0.0.1:8787/** and offer to open it. On Windows: `start http://127.0.0.1:8787/`; on macOS: `open http://127.0.0.1:8787/`.
5. Remind the founder they can click **Pop out** for a compact always-on-top window (Document Picture-in-Picture; Edge / Chrome / Firefox 151+), and that the language selector in the header changes the on-screen language.

## Notes
- Everything you tell the founder (workspace/Python checks, the viewer URL, next steps, stop confirmation) goes in their language — match the language the founder is writing in; never default to English or Japanese.
- **Japanese katakana:** keep the trailing long-vowel mark on loanwords ending in -er/-or/-ar — write **「ビューアー」** (not 「ビューア」), 「ブラウザー」 (not 「ブラウザ」), 「セレクター」, 「ヘッダー」. Do not drop the final ー.
- The server uses only the Python standard library — no installs needed.
- It serves on localhost only (127.0.0.1) and reads from the current workspace.
- Leave it running while you hold meetings. **To stop it, the founder just asks Claude Code to stop the viewer** — stop the local process listening on `127.0.0.1:8787` (use the OS-appropriate command). It was started in the background, so there is usually no terminal for the founder to Ctrl+C; Ctrl+C only applies if they started it themselves in a visible terminal.
