---
name: doctor
description: Check the Ainvis Local environment and fix it. Reports what works now and, if the optional boardroom viewer needs Python and it is missing, offers to install it for you. Run this if the viewer won't start.
---

# Ainvis Local — environment doctor

Check the environment and get it ready. The **boardroom viewer is a core part of the Ainvis experience** — the live, always-on-top window with the five executives is how it feels like Ainvis, and it's the bridge to the paid extensions and to Ainvis itself (the original edition). The viewer needs **Python** (it serves a local page so always-on-top Picture-in-Picture and the self-hosted Futura font work — these are non-negotiable, so there is no browser-only fallback). This skill makes that one-time setup effortless: Claude Code installs Python for you.

## Steps

1. Check Python. Run both and report:
   - `python --version`
   - `python3 --version`

2. **If Python is present**: confirm the viewer is ready and tell the founder to run `/ainvis-local:viewer`.

3. **If Python is NOT present**: explain it powers the boardroom viewer (always-on-top + Futura), then offer to install it (ask first — never install without consent):
   - **Windows**: `winget install -e --id Python.Python.3.13`
   - **macOS**: `brew install python` (or `python3` from the Xcode Command Line Tools: `xcode-select --install`)
   - **Linux**: distro package manager (e.g. `sudo apt install python3`).
   After installing, re-run the version check, then point to `/ainvis-local:viewer`.

4. Note for context: the text discussion (`/ainvis-local:meet`) runs even without Python, but the intended experience includes the live boardroom — so getting Python set up is part of a complete install.

## Rules
- Report everything to the founder in their language — the Python status, the results, and the next step must match the language the founder is writing in. Never default to English or Japanese.
- **Japanese katakana:** keep the trailing long-vowel mark on loanwords ending in -er/-or/-ar — write **「ビューアー」** (not 「ビューア」), 「ブラウザー」 (not 「ブラウザ」). Do not drop the final ー.
- Never install anything without explicit consent.
- This is something Claude Code does for the founder — they should not have to hunt for or configure Python by hand.
