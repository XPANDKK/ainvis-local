---
name: setup
description: Initialise an Ainvis Local workspace inside a dedicated `ainvis-local-workspace/` folder — creates the meetings/ minutes/ library/ structure and the decisions log. No config to fill in. Run this once before your first board meeting.
---

# Ainvis Local — Workspace setup

Set up the founder's board-meeting workspace inside a **dedicated `ainvis-local-workspace/` folder** in the current directory. There is **no configuration form to fill in** — the board learns about the company from the files the founder drops into `library/` and from the conversation, and asks when it needs to know something. Everything lives under this one folder, so it never litters the home or project root and is trivial to remove later. This is a one-time scaffold.

## Steps

1. **Place the workspace safely — never scatter files into the current directory.** The workspace is the single folder `./ainvis-local-workspace/`.
   - Always create the contained `ainvis-local-workspace/` folder and put everything inside it. Never create `meetings/`, `minutes/`, or `library/` directly in the current directory — this matters especially when the current directory is the user's home directory or a drive root (e.g. `C:\Users\<name>`, `C:\`, `/home/<name>`, `/`).
   - If `ainvis-local-workspace/` already exists with content (e.g. it has `decisions.md`), do NOT overwrite — tell the founder it is already set up (show its path) and stop.

2. Create the following structure (only what does not yet exist), all **inside `ainvis-local-workspace/`**:

```
ainvis-local-workspace/
├─ decisions.md
├─ meetings/          (empty — live + archived discussion logs)
├─ minutes/           (empty — formatted minutes, Markdown only)
├─ library/
│  ├─ general/        (company overview, goals, background)
│  ├─ ops/            (operational data, KPIs, action history — COO)
│  ├─ finance/        (models, budgets, board materials — CFO)
│  ├─ marketing/      (positioning, campaigns, market research — CMO)
│  ├─ tech/           (architecture notes, constraints — CTO)
│  └─ cx/             (customer feedback, usability notes — CXO)
└─ overlays/          (optional — your own per-executive prompt overlays, e.g. overlays/cfo-james.md)
```

3. Write `ainvis-local-workspace/decisions.md` with a header only:

```markdown
# Decisions Log

> Append-only. Each board meeting adds confirmed decisions here, newest at the bottom.
```

4. (Optional) Write `ainvis-local-workspace/library/general/README.md` to orient the founder:

```markdown
# Your reference library

Drop anything about your company here — overview, goals, numbers, plans, notes.
The board reads `library/` to ground its advice; the more you add, the more
specific it gets. Nothing is required — the board also asks when it needs to know
something. The domain folders (ops, finance, marketing, tech, cx) help the right
executive find the right material, but plain notes in `general/` are fine too.
```

   Also write `ainvis-local-workspace/overlays/README.md` so the founder can customise the executives:

```markdown
# Customise your executives (overlays)

Drop a file named after an executive here to add your own instructions, context,
tone, or focus to that person — it layers on top of their built-in character:

- `coo-wei.md`   — Chen, WeiNX3 (COO)
- `cmo-nova.md`  — Tan, NovaDL7 (CMO)
- `cfo-james.md` — Hart, JamesSG5 (CFO)
- `cto-dev.md`   — Patel, DevZT1 (CTO)
- `cxo-zola.md`  — Dlamini, ZolaEP9 (CXO)

The non-negotiable team charter (no name preambles, same-boat tone, facts only
from your `library/` and the conversation, own mistakes, follow your language)
always applies — overlays add and adjust, they don't override it.

Only files in *this* folder are ever loaded — nothing is applied automatically.
```

5. **Record the workspace location so the board can find it from anywhere.**
   - Resolve the workspace's **absolute** path (the current directory joined with `ainvis-local-workspace`).
   - Save it: write `{"workspace": "<absolute path>"}` to **`${CLAUDE_PLUGIN_DATA}/workspace.json`** (fallback `~/.ainvis-local/workspace.json`; `%USERPROFILE%\.ainvis-local\workspace.json` on Windows). Create the directory if needed. This is how `meet` and `viewer` locate the workspace later — **so the founder never has to `cd` into it.** (This write is outside the workspace, so Claude Code may ask permission once — that is expected.)
   - Then tell the founder (in their language) that setup is complete — everything lives in **`ainvis-local-workspace/`** and there is nothing to configure. They can run **`/ainvis-local:meet <topic>`** and **`/ainvis-local:viewer`** from anywhere — Ainvis Local finds this workspace automatically (no `cd` needed). To consult one executive, just address them, e.g. `/ainvis-local:meet CFO, <question>`. Optionally drop reference material into the `library/` subfolders; the board reads it and asks when it needs to know something. To remove Ainvis Local later: uninstall the plugin and delete the `ainvis-local-workspace/` folder (all data is contained there).

6. Note on setup (keep it brief): the board discussion runs in Claude Code. The **boardroom viewer is a core part of the experience** and needs Python (for the always-on-top window and Futura font). Run `/ainvis-local:doctor` once — it checks for Python and, if missing, installs it for you. Then `/ainvis-local:viewer` opens the boardroom.

## Rules
- **Write everything you show the founder in their language** — the setup-complete summary, the folder explanation, and the next-steps list must all match the language the founder is writing in (the same strict language-follow rule meet uses). Never default to English or Japanese.
- **Japanese katakana:** keep the trailing long-vowel mark on loanwords ending in -er/-or/-ar — write **「ビューアー」** (not 「ビューア」), 「ブラウザー」 (not 「ブラウザ」), 「ライブラリー」, 「フォルダー」. Do not drop the final ー.
- Never fabricate company facts — the board grounds in `library/` and what the founder tells it; when something is unknown, it asks.
- Respect existing files — this skill must be safe to run in a folder that already has content.
- **Always contain everything in `ainvis-local-workspace/` — never scatter files into the current directory or the user's home.**
