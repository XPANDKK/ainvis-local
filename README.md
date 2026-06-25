# Ainvis Local

**Your five-executive founding team, on your own machine.** Discuss strategy with a board of COO, CTO, CFO, CMO and CXO advisors — entirely from local files, no cloud account, no subscription to us. Works with [Claude Code](https://claude.com/claude-code).

> Early days — Phase 0. The core works; expect a few rough edges while it settles.

## What it is

Ainvis Local is a Claude Code plugin. It gives you a standing board of five executive advisors — each a distinct character with their own expertise and a shared founder-team charter — that you convene from inside Claude Code. Everything stays on your machine:

- **Discussion** happens in Claude Code, in your language — an ordinary conversation, not a debate.
- **Records** (meeting logs, minutes, decisions) are written as plain Markdown in your workspace.
- **Your reference material** in `library/` is read directly by the executives (local RAG — no vector database, no upload).
- **A live boardroom viewer** shows the five executives talking as the meeting unfolds — a compact, always-on-top window beside Claude Code.

It runs on your own Claude Pro/Max subscription (or API key) — the only LLM cost is yours, and there is no server of ours in the loop.

## The board

| Persona | Role | Owns |
|---|---|---|
| Chen, WeiNX3 | COO | execution, KPIs, operational cadence |
| Patel, DevZT1 | CTO | technology strategy, architecture, security |
| Hart, JamesSG5 | CFO | financial planning, cash flow, risk |
| Tan, NovaDL7 | CMO | brand, demand generation, go-to-market |
| Dlamini, ZolaEP9 | CXO | customer experience, usability, the human side |

Convene the whole board, or address one executive directly for a deeper one-to-one — both happen inside `meet`. The executives build on each other and disagree, like a real founding team; they don't stage a formal debate.

## Quick start

> Install from the **Claude Code CLI** (run `claude` in your terminal). `/plugin` is a Claude Code feature — if you don't have the CLI, get it at https://claude.com/claude-code.

1. In Claude Code, add this plugin's marketplace and install it:
   ```
   /plugin marketplace add https://github.com/XPANDKK/ainvis-local
   /plugin install ainvis-local@ainvis-local-marketplace
   ```
   - When asked **where to install**, choose **"Install for you (user scope)"** — the board becomes available in all your projects. (Choose *project scope* only to share it with collaborators on one repository, or *local scope* for a single repository on your machine.)
   - If the preview shows *"Components will be discovered at installation"*, that is expected — the five executives, skills and hooks are detected automatically.
   - **After installing, restart Claude Code** to activate the plugin (a full restart loads the skills and hooks reliably — `/reload-plugins` alone may report *0 skills*). Until activated, the `/ainvis-local:…` commands show as *Unknown command*.
2. Scaffold a workspace and set up the viewer:
   ```
   /ainvis-local:setup
   /ainvis-local:doctor
   ```
   `setup` creates an **`ainvis-local-workspace/`** folder — all your board data lives in this one folder (nothing is scattered into your home or project root). There is **nothing to configure**: optionally drop reference material about your company into `library/` (the board reads it, and asks when it needs to know something). `doctor` checks for Python (needed for the boardroom viewer) and installs it if missing. You can run `meet` / `viewer` **from anywhere** — Ainvis Local finds this workspace automatically (no `cd` needed).
3. Convene the board:
   ```
   /ainvis-local:meet should we keep building the local edition or refocus?
   ```
   Or consult one executive directly — just address them inside `meet`:
   ```
   /ainvis-local:meet CFO, can we afford one more month of runway?
   ```
4. Open the boardroom viewer — the live, branded boardroom (a core part of the experience):
   ```
   /ainvis-local:viewer
   ```
   It serves http://127.0.0.1:8787/; click **Pop out** for a compact, always-on-top window beside Claude Code. Your own turns appear highlighted with timestamps, and the interface follows the meeting's language (40+ languages); when the window is minimised, a notification brings each new turn to you. (Runs a small local Python server — set up once via `/ainvis-local:doctor`.) To stop it, just ask Claude Code to stop the viewer.
5. Wrap up to keep the minutes — just tell the board you're done (e.g. "let's wrap up") and Ainvis Local saves clean minutes (key points, decisions, action items) to your `minutes/` folder and records the decisions, so the board carries them into the next meeting. Open past meetings from the viewer's **Past meetings** link.

## Workspace layout

```
decisions.md         append-only log of board decisions
meetings/            discussion logs (live + archived)
minutes/             formatted minutes (Markdown)
library/
  general/  ops/  finance/  marketing/  tech/  cx/   your reference material
```

Put your workspace in a synced folder (OneDrive, Box, …) and you can read the minutes from your phone.

## Customise the board

Want an executive to know your context or speak in a particular way? Drop a file in your workspace's `overlays/` folder named after them — `overlays/cfo-james.md`, `overlays/cto-dev.md`, and so on. Whatever you write layers on top of their built-in character. The team charter (same-boat tone, honesty, no fabrication, your language) always applies — overlays add and adjust, they don't override it. (Ainvis Local is Apache-2.0, so good overlays can be shared back.)

## Free, and local-first

The whole core — the five executives, discussions, minutes, decisions log and local RAG — is **free**, on your own Claude subscription. No trial, no card. Your whole history is plain Markdown, so when you need a team edition — shared access, enterprise-grade security, voice on Web and Microsoft Teams, and access from any device — you can step up to the cloud **Ainvis** and your board picks up right where you left off.

> An optional local voice capability (speech-in / speech-out) is under consideration, not yet decided.

## Uninstall

In Claude Code:
```
/plugin marketplace remove ainvis-local-marketplace
```
Removing the marketplace uninstalls the plugin (or uninstall it alone from the `/plugin` **Installed** tab). Uninstalling never touches your data — to remove that too, delete the **`ainvis-local-workspace/`** folder, where everything Ainvis Local wrote lives.

## Licence & trademarks

Apache-2.0 (see `LICENSE` / `NOTICE`). "Ainvis" is a trademark of XPAND K.K. "Claude" and "Claude Code" are trademarks of Anthropic; this project is independent and not affiliated with Anthropic, and only states compatibility ("Works with Claude Code").
