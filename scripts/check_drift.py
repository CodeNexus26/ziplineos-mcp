#!/usr/bin/env python3
"""Compare scripts/known-tools.txt with a live MCP tools/list call.

Fails if a tool the docs and skills rely on no longer exists on the server. Prints, without
failing, any new server tool that isn't documented yet.

Environment:
  MCP_DRIFT_URL    MCP endpoint to check (e.g. a test environment).
  MCP_DRIFT_TOKEN  Bearer access token for a test account on that environment.
"""
import json
import os
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = os.environ.get("MCP_DRIFT_URL", "")
TOKEN = os.environ.get("MCP_DRIFT_TOKEN", "")
if not URL or not TOKEN:
    print("MCP_DRIFT_URL / MCP_DRIFT_TOKEN not set; skipping drift check.")
    sys.exit(0)

session_id = None


def rpc(method: str, params: dict | None = None, notify: bool = False):
    global session_id
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notify:
        body["id"] = 1
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {TOKEN}",
        "MCP-Protocol-Version": "2025-06-18",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        session_id = resp.headers.get("Mcp-Session-Id") or session_id
        raw = resp.read().decode("utf-8")
        if notify:
            return None
        if resp.headers.get("Content-Type", "").startswith("text/event-stream"):
            payloads = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
            raw = next(p for p in payloads if '"id"' in p)
        msg = json.loads(raw)
        if "error" in msg:
            raise SystemExit(f"{method} failed: {msg['error']}")
        return msg["result"]


rpc("initialize", {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "ziplineos-mcp-drift-check", "version": "1"},
})
rpc("notifications/initialized", notify=True)
live, cursor = set(), None
while True:
    result = rpc("tools/list", {"cursor": cursor} if cursor else {})
    live |= {t["name"] for t in result.get("tools", [])}
    cursor = result.get("nextCursor")
    if not cursor:
        break

known = {
    l.strip()
    for l in (ROOT / "scripts/known-tools.txt").read_text(encoding="utf-8").splitlines()
    if l.strip() and not l.startswith("#")
}
missing = sorted(known - live)
new = sorted(live - known)
if new:
    print("New server tools not yet documented (consider updating the skills):", ", ".join(new))
if missing:
    print("Documented tools missing from the server:", ", ".join(missing))
    sys.exit(1)
print(f"OK: all {len(known)} documented tools exist on the server.")
