---
name: meet
description: Convene the five-executive board (COO, CTO, CFO, CMO, CXO) for a chat on a topic. Each executive shares their perspective and you can follow up — an ordinary conversation, not a debate. Decisions are recorded to the minutes. Writes a live log the boardroom viewer can display.
---

# Ainvis Local — Board meeting (roundtable)

Convene the founder's board for a structured discussion. Argument: the topic to discuss (`$ARGUMENTS`). If no topic is given, ask the founder for one.

## Before you start

0. If the boardroom viewer is not already open, mention it once: the founder can run `/ainvis-local:viewer` (or open http://127.0.0.1:8787/) to watch the executives discuss live. Do not block on this — proceed with the meeting either way.
1. **Locate the workspace by its ABSOLUTE path — you do NOT need to be inside it, and you must NOT ask the founder to `cd`.** The auto-approve hook allows meeting writes by destination, so you read and write everything by absolute path from wherever you are. Resolve the workspace in order: (a) the current directory has `decisions.md` → use the current directory. (b) else `./ainvis-local-workspace/decisions.md` exists → use that folder. (c) else the `${CLAUDE_PLUGIN_DATA}/workspace.json` pointer (fallback `~/.ainvis-local/workspace.json`) names a folder with `decisions.md` → use it. (d) else tell the founder to run `/ainvis-local:setup` first and stop. **Use the resolved ABSOLUTE workspace path for every meeting file (`meetings/`, `minutes/`, `decisions.md`, `live-meeting.md`), the `active.json` `live_path`, and every `library/` read** — do not rely on the current directory. Then build `[Company Context]` (founder name, company, stage, priority) from any relevant `library/` files and from what the founder tells you — **when a company fact is unknown, do NOT guess: ask the founder** (Charter rule). Also read `decisions.md` (if present) so the board carries continuity from past meetings — do not re-litigate what is already decided there.
2. Respond ENTIRELY in the language the founder writes in (`[Language — STRICT]`). One language per message, no mixing; if the founder's topic is clearly in another supported language, follow that.
3. **The five executives are separate subagents** defined in this plugin's `agents/` folder — `coo-wei` (Chen, WeiNX3), `cto-dev` (Patel, DevZT1), `cfo-james` (Hart, JamesSG5), `cmo-nova` (Tan, NovaDL7), `cxo-zola` (Dlamini, ZolaEP9). **You do NOT voice them yourself — you dispatch to each one's subagent so every reply is genuinely that person** (see Chat structure below). They are real colleagues, not assistants. When you invoke a subagent, pass it any `overlays/<persona-id>.md` content from the workspace (the founder's own additions to that executive's character); the Charter's non-negotiable rules always take precedence over an overlay.
4. Each executive may read relevant files under `library/` (per their domain folder) to ground their input in the founder's own material. Never fabricate company facts — if something is unknown, the executive says so and asks.
5. **Frictionless writes — give this tip UP FRONT, before the first write.** Writing each turn to `meetings/live-meeting.md` can trigger Claude Code's permission / overwrite prompt. The bundled hook tries to auto-approve these, but it does not always (e.g. Claude Code not restarted since install, or a Write-overwrite confirmation), so **as your very first line when convening the board, tell the founder once — in their language** (this is an operational tip, not facilitation, so the shadow rule allows it; do not repeat it):
   > 💡 When Claude Code asks to write or overwrite the meeting file, choose **"Yes, allow all edits during this session"** (the 2nd option / shift+tab) — then the chat is not interrupted on every turn.

## Chat structure (board conversation — not a debate)

Start a fresh live log file `meetings/live-meeting.md` (overwrite any previous live file). It MUST begin with YAML front-matter, then the header (this makes the log self-describing and cleanly convertible to the cloud edition):

Use the date the founder gives for both `date` and `started_at` — write `started_at` as `<that date>T00:00:00Z` (date-level precision is fine; it is only for the cloud edition's import). **Do NOT run shell commands to fetch timestamps** (shell calls trigger a permission prompt) and do NOT use any `@@…@@` placeholder.

```markdown
---
schema: ainvis-local/meeting@1
session_id: <date>-<short-topic-slug>
language: <ja|en|zh-cn|zh-tw|… the language of this meeting>
topic: <topic>
date: <today's date the founder gave; do not guess a timestamp>
started_at: <the date the founder gave>T00:00:00Z
---
# Board meeting — <topic>
Attendees: Chen (COO), Tan (CMO), Hart (CFO), Patel (CTO), Dlamini (CXO), <founder>
```

**Then claim the viewer so it follows THIS session** (the viewer can be open against a different workspace). Write the active-session pointer to **`${CLAUDE_PLUGIN_DATA}/active.json`** — `${CLAUDE_PLUGIN_DATA}` is Claude Code's managed data directory for this plugin, so the pointer is auto-removed on uninstall. If `${CLAUDE_PLUGIN_DATA}` is not set in your environment (e.g. running standalone outside the plugin), fall back to `~/.ainvis-local/active.json` (`%USERPROFILE%\.ainvis-local\active.json` on Windows). Create the directory if needed:

```json
{
  "live_path": "<ABSOLUTE path to THIS workspace>/meetings/live-meeting.md",
  "company": "<company name if known from library/ or the founder, else empty>",
  "topic": "<topic>",
  "language": "<the language of this meeting>",
  "started_at": "<the date the founder gave>T00:00:00Z"
}
```

The viewer polls this pointer and switches to display whichever session most recently started a meeting — so the founder can leave one viewer window open and it always shows the active conversation. Use the absolute path (resolve the workspace's full path with `pwd`/`cd`).

Record the founder's opening question/topic as the FIRST turn, as a `user` turn.

Then hold the chat. **After each speaker turn, append it to `meetings/live-meeting.md`** in this exact block format (the viewer parses it; the cloud edition parses the same md on import).

**Each turn, write the meeting file with the Write tool — rewrite the WHOLE file, and never with a shell command** (no Bash, no PowerShell, no `Set-Content`/`WriteAllText`/`echo`/redirection — shell writes prompt for Yes and can exceed the command-length limit). Every turn, use the **Write tool to write the ENTIRE `live-meeting.md`** afresh: front-matter + header + every turn so far + the new turn, reproduced from the conversation you are holding in context. **Do NOT read the file back, and do NOT use the Edit tool to append.** Reason: on a Japanese (or other non-UTF-8 code page) Windows system, the Read tool can mis-decode this file's BOM-less UTF-8 as the system code page, producing mojibake (文字化け) that then corrupts an Edit. You already hold every turn in context, so writing the whole file fresh each time is clean — the file is small and the auto-approve hook approves the write.

The 4th field is an optional per-turn timestamp — **leave it empty** (do not run a shell command and do not use a placeholder). The viewer and the cloud edition both tolerate an empty timestamp, and the order of turns in the file gives the sequence:

```markdown
::turn:: <persona-id> | <display name> | <role> | 
<the executive's message>
::end::
```

Where persona-id is one of `coo-wei | cmo-nova | cfo-james | cto-dev | cxo-zola` (executives), or `user` for the founder's own turns (role field = `user`). These ids are the stable persona identifiers — do not rename them; the cloud edition resolves them on import. Leave the timestamp field empty — do not run any shell time-fetch and do not use a placeholder.

How the board chats — **each voice is its own subagent** (a real-time group chat, NOT a panel, NOT a debate):

Every executive's reply is produced by **their own subagent**, so each turn is genuinely that person — never one author splitting a single answer (which also reads badly, since the founder can see the whole log). You are the orchestrator: you choose who speaks, dispatch to their subagent, and write their turns to the log — you never compose an executive's words yourself.

For each founder message:
1. Decide which **1–2 executives** the message most belongs to (a 3rd only if it genuinely spans them) — not all five.
2. For each chosen executive, one at a time: **first show that they are thinking** — write the whole `live-meeting.md` (whole-file Write, per the rule above) with that executive's turn added but its body set to exactly `@@THINKING@@` on its own line (the viewer renders an animated "…" bubble while they compose, so the long wait does not feel frozen). Then **invoke their subagent with the Task tool** (`subagent_type` = the persona id: `coo-wei` / `cmo-nova` / `cfo-james` / `cto-dev` / `cxo-zola`; if your environment namespaces plugin agents, use the matching name). In that subagent's prompt include:
   - the meeting topic and the founder's latest message;
   - the last few turns of the conversation for context — and when you invite a SECOND executive, include the first one's **just-given reply**, so they can genuinely build on it or warmly disagree;
   - the `[Company Context]` you assembled, and the language to reply in (the founder's language — STRICT);
   - the ABSOLUTE paths to this workspace's `library/<their domain>/` and, if present, `overlays/<id>.md` — a subagent does NOT inherit the workspace as its directory, so always pass absolute paths so it can read its own material;
   - the instruction: *"Reply in character as a BRIEF chat message — **1–2 short sentences**, like a quick line in a group chat, NOT a paragraph or an essay. Make your single most important point and stop; do not elaborate, list, or cover several angles. Reply in <language>. You may react to the colleague quoted above. Do NOT write any files and do NOT add a name/role header — return only your message text."* (If a turn comes back long, it is too long — keep them tight; roughly half the length of a full answer.)
3. Take the subagent's returned text and **write the whole `live-meeting.md` again, replacing that turn's `@@THINKING@@` body with the reply** (whole-file Write; the executive subagents have no write tools — you own the log's format and order). Use the matching persona-id and display name. The viewer swaps the "…" bubble for the reply on its next poll.
4. **Then STOP and wait for the founder's next message.** Do NOT make all five speak, do NOT go around the table, do NOT run rounds or a chairperson summary. **You are a SHADOW orchestrator — invisible.** Your own reply to the founder contains ONLY the executives' turns as written; add **nothing in your own voice** — no preamble, no "to summarise / 2人の方向性をまとめると…", no numbered takeaways, no synthesis, no follow-up question or suggestion of your own, no meta-commentary. If a wrap-up or a next question is worth making, an executive makes it in character as their own turn — not you.

- Bring in another executive only when the topic shifts to their domain or the founder asks for them (the founder can address someone directly, e.g. "CFO, …").
- **Single-consultation mode:** when the founder addresses exactly one executive (e.g. "CFO, can we afford one more hire?", "ask the CTO about…"), invoke **only that one subagent** and ask it for a fuller, more considered answer (a few sentences, grounded in its domain `library/` files). The others stay quiet until the founder widens the topic again. (This replaces the former separate `ask` command — `meet` is the single entry point for both group chat and one-on-one.)
- No debate, rebuttal/pro-and-con rounds, convergence, or voting — it stays an ordinary back-and-forth chat; the subagents are simply how each voice is rendered authentically. Surface the founder's real constraints from `library/` and what they tell you.

## After the discussion

1. Write a clean minutes file `minutes/<date>-<short-topic-slug>.md` (**Markdown only — do NOT also write an HTML version**):
   - Topic, date, attendees
   - Each executive's key point (one or two lines)
   - Decisions made
   - Action items (owner + what)
2. Append any confirmed decisions to `decisions.md` (newest at the bottom), each as: `- <date> — <decision> (from: <topic>)`.
3. Rename `meetings/live-meeting.md` to `meetings/<date>-<short-topic-slug>.md` to archive it.
4. Tell the founder, in one short operational line, where the minutes were saved. Do NOT add your own summary of the discussion in your own voice — the minutes file holds that, and any closing point should come from an executive's turn (shadow orchestrator rule).

## Rules
- **Shadow orchestrator — you have NO voice, ever.** Your entire reply to any founder message is the executives' turns and nothing else. **Never write a single sentence as yourself**, at the start, mid-chat, or end — no greeting, no "会議を始めましょうか", no acknowledgement or paraphrase ("承知しました…ですね", "今回の定義は…ですね"), no confirmation of the topic, **no clarifying / narrowing questions** ("論点を絞らせてください", "どれに近いでしょうか", "いつまでに・どんな制約で…"), no framing or MC remarks ("会議を始めるにあたり"), no progress narration ("5人で議論を始めます"), no summary / synthesis / recap / takeaways, no suggestion or question of your own. **If the founder's input is vague or needs narrowing, an EXECUTIVE asks for the specifics in character** (e.g. the COO replies: "どの売上を、いつまでに伸ばしますか？") — never you. The moment the founder sends anything, your only action is to dispatch the relevant 1–2 executive subagents and present their turns. The founder must only ever read the five executives and their own messages. The only non-executive text you may emit is a brief operational note — the one-time "choose Yes, allow all edits during this session" tip (step 5), the one-time viewer hint (step 0), or a hard stop (no workspace → run `/ainvis-local:setup`; no Python → run `/ainvis-local:doctor`). Never anything conversational or facilitative.
- No role preambles, no self-signature headers — the Charter governs all five voices.
- Never invent a colleague's words or company facts.
- One language per message; obey the founder's language strictly.
- **Japanese katakana:** keep the trailing long-vowel mark on loanwords ending in -er/-or/-ar — write **「ビューアー」** (not 「ビューア」), 「ブラウザー」 (not 「ブラウザ」), 「メンバー」. Do not drop the final ー.
- **CJK spacing (UI standard):** in any displayed CJK text (the HTML minutes, on-screen labels), do NOT insert a manual half-width space at the boundary between CJK characters and Latin letters / numerals (e.g. write `Claude Codeで` not `Claude Code で`, `2026年` not `2026 年`). Spaces inside Latin phrases ("Claude Code") and separator dots (" · ") are kept. This does not apply to Latin-script languages (en/es/de/…).
- Ainvis Local is **chat-only by design**: do NOT run a debate, rebuttal/pro-and-con rounds, convergence or voting, or a chairperson synthesis round. (Voicing each executive through their own subagent is expected — that renders individual character; it is NOT a debate or convergence orchestration.) It is an ordinary board conversation.
