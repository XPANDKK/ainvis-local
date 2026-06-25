#!/usr/bin/env python3
"""Ainvis Local — PreToolUse auto-approve for frictionless board meetings.

Scoped, default-on. Auto-approves only the board's read-only tools and the
meeting file writes whose DESTINATION is inside an Ainvis Local workspace (a
directory tree containing decisions.md) — independent of the session cwd, since
Claude Code resets cwd to the project root when it leaves it, so a workspace
opened from elsewhere never becomes cwd. Everything else defers to the normal
Claude Code permission flow. Fails open (never blocks).
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

# The five board personas (custom subagents). Launching one via the Agent/Task
# tool is auto-approved so each board turn doesn't prompt. The subagent itself
# has only Read/Grep/Glob, and its inner reads are gated like any other read.
_PERSONA_AGENTS = frozenset({"coo-wei", "cmo-nova", "cfo-james", "cto-dev", "cxo-zola"})
# tool_input keys that might carry the subagent type (subagent_type is the Agent
# tool's documented param; the hook payload field is undocumented, so try aliases).
_AGENT_TYPE_KEYS = ("subagent_type", "subagentType", "agent_type", "agentType", "type", "agent", "name")


def _emit_allow() -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }))


def _within(child: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def _workspace_root(path: pathlib.Path) -> "pathlib.Path | None":
    """Nearest ancestor (including the path's own directory) that marks an Ainvis
    Local workspace by containing decisions.md. Bounded upward walk; returns None
    if not found. Works for not-yet-created files (walks from the parent dir)."""
    try:
        start = path if (path.exists() and path.is_dir()) else path.parent
        cur = start.resolve()
    except OSError:
        return None
    for _ in range(40):  # safety bound against pathological depth
        try:
            if (cur / "decisions.md").exists():
                return cur
        except OSError:
            return None
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError, OSError):
        sys.exit(0)  # malformed input -> defer to normal prompt

    req = data.get("tool_use_request") or {}
    tool = data.get("tool_name") or req.get("tool_name")
    tin = data.get("tool_input") or req.get("tool_input") or {}
    if not isinstance(tin, dict):
        tin = {}

    cwd = pathlib.Path(data.get("cwd") or os.getcwd())
    plugin_root_env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    plugin_root = pathlib.Path(plugin_root_env) if plugin_root_env else None

    file_path = tin.get("file_path") or tin.get("path")

    # Never auto-approve protected paths.
    if file_path and any(
        seg in str(file_path).replace("\\", "/") for seg in ("/.claude/", "/.git/")
    ):
        sys.exit(0)

    # Sub-agent launches (Agent/Task tool): auto-approve ONLY the five board
    # personas, so each board turn doesn't trigger a Yes/No prompt. The persona
    # subagents have only Read/Grep/Glob; their inner reads are gated like any
    # other read (by workspace destination). The type field name in the hook
    # payload is undocumented, so check several keys and allow only an exact
    # persona id (tolerating a namespace like "ainvis-local:coo-wei").
    if tool in ("Agent", "Task"):
        for _k in _AGENT_TYPE_KEYS:
            _v = tin.get(_k)
            if isinstance(_v, str) and _v.split(":")[-1].split("/")[-1] in _PERSONA_AGENTS:
                _emit_allow()
                break
        sys.exit(0)

    # Scope is the TARGET's workspace, not the session cwd (Claude Code resets cwd
    # to the project root when it leaves it, so a workspace opened from elsewhere
    # never becomes cwd; gating on cwd meant every turn prompted). A workspace is a
    # directory tree containing decisions.md.

    # Read-only tools: inside any Ainvis Local workspace, or the plugin's bundled files.
    if tool in ("Read", "Grep", "Glob"):
        target = pathlib.Path(file_path) if file_path else cwd
        if not target.is_absolute():
            target = cwd / target
        if _workspace_root(target) is not None or (plugin_root and _within(target, plugin_root)):
            _emit_allow()
        sys.exit(0)

    # Writes: only the meeting outputs, and only when the destination is inside a workspace.
    if tool in ("Write", "Edit") and file_path:
        target = pathlib.Path(file_path)
        if not target.is_absolute():
            target = cwd / target
        ws = _workspace_root(target)
        if ws is not None:
            try:
                rel = target.resolve().relative_to(ws.resolve())
                if rel.parts and (
                    rel.parts[0] in ("meetings", "minutes")
                    or target.name in ("decisions.md", "live-meeting.md")
                ):
                    _emit_allow()
            except (ValueError, OSError):
                pass
        sys.exit(0)

    # Bash and everything else -> defer to the normal permission flow.
    sys.exit(0)


if __name__ == "__main__":
    main()
