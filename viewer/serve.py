#!/usr/bin/env python3
"""Ainvis Local — boardroom viewer server (Phase 0 PoC).

Serves the boardroom viewer page and the live meeting log over localhost,
using only the Python standard library (no pip installs). Run it from your
Ainvis Local workspace directory:

    python <plugin>/viewer/serve.py

then open http://127.0.0.1:8787/ in a browser. The page polls the live log
and renders each executive's turn as they speak. Click "Pop out" to float a
compact always-on-top window (Document Picture-in-Picture; Edge / Chrome / Firefox 151+).

This is a Phase 0 proof-of-concept. The shipped product serves the same page
from the plugin's bundled MCP server; this standalone script exists so the
boardroom UX can be validated without extra dependencies.
"""
from __future__ import annotations

import html
import http.server
import json
import os
import pathlib
import socketserver
import urllib.parse

PORT = 8787
VIEWER_DIR = pathlib.Path(__file__).resolve().parent
WORKSPACE = pathlib.Path.cwd()
LIVE_LOG = WORKSPACE / "meetings" / "live-meeting.md"

# Global active-session pointer — lets one viewer follow whichever Claude Code
# session is currently in a meeting, even across different workspaces. The meet
# skill writes this at meeting start: {"live_path": "<abs path to that
# workspace's meetings/live-meeting.md>", "topic": ..., "company": ..., ...}.
# Stored in Claude Code's managed plugin-data dir (CLAUDE_PLUGIN_DATA) so it is
# auto-removed on uninstall; falls back to ~/.ainvis-local for standalone dev
# when the env var is not set.
_PLUGIN_DATA = os.environ.get("CLAUDE_PLUGIN_DATA")
# The meet / setup skills write active.json / workspace.json into Claude Code's
# managed plugin-data dir (CLAUDE_PLUGIN_DATA). serve.py runs as a subprocess
# that may NOT inherit that env var, so look in several candidate homes — the
# env dir, the KNOWN managed-data path (even without the env var), and the
# standalone fallback. Without this the viewer looked in ~/.ainvis-local while
# meet wrote the managed dir, so /live.md came back empty.
_MANAGED_DATA = (pathlib.Path.home() / ".claude" / "plugins" / "data"
                 / "ainvis-local-ainvis-local-marketplace")
_STANDALONE_DATA = pathlib.Path.home() / ".ainvis-local"


def _read_pointer(name: str):
    """Read a pointer json (active.json / workspace.json) from the first home
    that has it: env CLAUDE_PLUGIN_DATA, then the managed-data path, then the
    standalone fallback. Returns the parsed dict, or None."""
    cands = []
    if _PLUGIN_DATA:
        cands.append(pathlib.Path(_PLUGIN_DATA) / name)
    cands.append(_MANAGED_DATA / name)
    cands.append(_STANDALONE_DATA / name)
    for p in cands:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
    return None


def resolve_live_log() -> pathlib.Path | None:
    """Path of the live log to display.

    Prefer the global active-session pointer so the viewer follows whichever
    session is meeting right now (Ainvis Local is solo, so one meeting at a
    time). Fall back to the workspace this server was launched in.
    """
    data = _read_pointer("active.json")
    if data:
        try:
            p = data.get("live_path")
            if p and pathlib.Path(p).exists():
                return pathlib.Path(p)
        except OSError:
            pass
    return LIVE_LOG if LIVE_LOG.exists() else None


def resolve_workspace() -> str | None:
    """OS-native absolute path of the workspace, for the viewer's cd hint.

    Order (mirrors the meet/viewer skills): the directory this server runs in
    (if it is a workspace), then the setup-recorded pointer, then the active
    meeting's workspace. Returns None if it cannot be determined.
    """
    if (WORKSPACE / "decisions.md").exists():
        return str(WORKSPACE)
    data = _read_pointer("workspace.json")
    if data:
        try:
            p = data.get("workspace")
            if p and (pathlib.Path(p) / "decisions.md").exists():
                return str(pathlib.Path(p))
        except OSError:
            pass
    data = _read_pointer("active.json")
    if data:
        try:
            lp = data.get("live_path")
            if lp:
                ws = pathlib.Path(lp).parent.parent  # <ws>/meetings/live-meeting.md
                if (ws / "decisions.md").exists():
                    return str(ws)
        except OSError:
            pass
    return None


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    _TYPES = {
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
    }

    def do_GET(self) -> None:  # noqa: N802 (stdlib API)
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            try:
                body = (VIEWER_DIR / "index.html").read_bytes()
            except OSError:
                self._send(500, b"index.html not found", "text/plain; charset=utf-8")
                return
            self._send(200, body, "text/html; charset=utf-8")
        elif path.startswith("/live.md"):
            live = resolve_live_log()  # follows the active session via the pointer
            text = live.read_text(encoding="utf-8") if live else ""
            self._send(200, text.encode("utf-8"), "text/markdown; charset=utf-8")
        elif path == "/workspace":
            # Absolute workspace path for the empty-state `cd "<abs>"` hint chip.
            ws = resolve_workspace()
            body = json.dumps({"workspace": ws or ""}).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        elif path.startswith("/assets/"):
            # Serve bundled viewer assets (logo, fonts). Reject path traversal.
            rel = path[len("/assets/"):]
            target = (VIEWER_DIR / "assets" / rel).resolve()
            assets_root = (VIEWER_DIR / "assets").resolve()
            if assets_root not in target.parents or not target.is_file():
                self._send(404, b"not found", "text/plain; charset=utf-8")
                return
            ctype = self._TYPES.get(target.suffix, "application/octet-stream")
            self._send(200, target.read_bytes(), ctype)
        elif path == "/minutes" or path.startswith("/minutes/"):
            # Past-meeting history — a simple browsable listing of the workspace's
            # minutes/ folder (no resume; the cloud edition handles that).
            # Resolve the workspace via the pointers (cwd-independent), falling
            # back to the launch directory if none is known.
            _ws = resolve_workspace()
            minutes_root = (pathlib.Path(_ws) if _ws else WORKSPACE).joinpath("minutes").resolve()
            rel = path[len("/minutes/"):] if path.startswith("/minutes/") else ""
            if rel == "":
                items = (
                    sorted(p.name for p in minutes_root.iterdir() if p.is_file())
                    if minutes_root.is_dir() else []
                )
                rows = "".join(
                    f'<li><a href="/minutes/{urllib.parse.quote(n)}">{html.escape(n)}</a></li>'
                    for n in items
                ) or "<li>No meetings yet.</li>"
                page = (
                    "<!doctype html><html lang=en><meta charset=utf-8>"
                    "<meta name=viewport content='width=device-width,initial-scale=1'>"
                    "<title>Ainvis Local &mdash; Past meetings</title><style>"
                    "@font-face{font-family:'Futura';font-weight:400;font-display:swap;"
                    "src:url('https://ainvis.ai/static/fonts/TT0142M.woff2?v=1') format('woff2')}"
                    "@font-face{font-family:'Futura';font-weight:700;font-display:swap;"
                    "src:url('https://ainvis.ai/static/fonts/TT0144M.woff2?v=1') format('woff2')}"
                    "body{font-family:'Futura','Century Gothic','Trebuchet MS',sans-serif;"
                    "background:#090912;color:#e4e4f0;margin:0;padding:1.6rem 1.25rem;line-height:1.6}"
                    "h2{font-size:18px;font-weight:700;margin:0 0 14px}"
                    "a{color:#22d3ee;text-decoration:none}a:hover{text-decoration:underline}"
                    "ul{list-style:none;padding:0;margin:0;max-width:720px}"
                    "li{border:1px solid #252540;background:#10101c;border-radius:8px;padding:10px 14px;margin:6px 0}"
                    ".muted{color:#5e5e80;font-size:12px;margin-top:16px}</style>"
                    "<body><h2>Ainvis Local &mdash; Past meetings</h2><ul>" + rows + "</ul>"
                    "<p class=muted>minutes/ &middot; read-only</p></body></html>"
                )
                self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
                return
            target = (minutes_root / rel).resolve()
            if minutes_root not in target.parents or not target.is_file():
                self._send(404, b"not found", "text/plain; charset=utf-8")
                return
            ctype = "text/html; charset=utf-8" if target.suffix == ".html" else "text/markdown; charset=utf-8"
            self._send(200, target.read_bytes(), ctype)
        else:
            self._send(404, b"not found", "text/plain; charset=utf-8")

    def log_message(self, *args: object) -> None:  # silence per-request logging
        return


def main() -> None:
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Ainvis Local viewer: http://127.0.0.1:{PORT}/  (workspace: {WORKSPACE})")
        print("Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")


if __name__ == "__main__":
    main()
