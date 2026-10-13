#!/usr/bin/env python3
"""Offline checks for this repository. Exit code 1 on any failure.

- Every *.json file parses.
- Marketplace and plugin manifests have the required fields, and their names match.
- The plugin .mcp.json declares each server with a type and a URL.
- Every SKILL.md has frontmatter with a valid name (matching its folder) and a description,
  and only uses keys that claude.ai skill upload accepts.
- The declarative-agent instruction.txt is identical to microsoft/agent-instructions.md.
- Every tool name mentioned in the skills and instructions is in scripts/known-tools.txt.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


# 1. All JSON parses.
for p in ROOT.rglob("*.json"):
    if ".git" in p.parts or "node_modules" in p.parts:
        continue
    load_json(p)

# 2. Marketplace + plugin manifests.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
market = load_json(ROOT / ".claude-plugin/marketplace.json") or {}
for key in ("name", "owner", "plugins"):
    if key not in market:
        err(f"marketplace.json: missing '{key}'")
if not (market.get("owner") or {}).get("name"):
    err("marketplace.json: owner.name is required")
for entry in market.get("plugins", []):
    name, source = entry.get("name"), entry.get("source", "")
    if not name or not NAME_RE.match(name):
        err(f"marketplace.json: plugin name '{name}' must be kebab-case")
    if not source.startswith("./") or ".." in source:
        err(f"marketplace.json: plugin '{name}' source must start with './' and not contain '..'")
        continue
    plugin_dir = ROOT / source
    manifest = load_json(plugin_dir / ".claude-plugin/plugin.json") or {}
    if manifest.get("name") != name:
        err(f"{source}/.claude-plugin/plugin.json: name '{manifest.get('name')}' != marketplace entry '{name}'")
    for key in ("version", "description", "author"):
        if key not in manifest:
            err(f"{source}/.claude-plugin/plugin.json: missing '{key}'")
    mcp_path = plugin_dir / ".mcp.json"
    if mcp_path.exists():
        mcp = load_json(mcp_path) or {}
        for sname, server in (mcp.get("mcpServers") or {}).items():
            if server.get("type") not in ("http", "streamable-http"):
                err(f"{source}/.mcp.json: server '{sname}' needs type 'http'")
            if not str(server.get("url", "")).startswith("https://"):
                err(f"{source}/.mcp.json: server '{sname}' needs an https url")

# 3. Skill frontmatter.
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
skill_files = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
if not skill_files:
    err("no skills found under plugins/*/skills/")
for skill in skill_files:
    rel = skill.relative_to(ROOT)
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{rel}: missing YAML frontmatter")
        continue
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    extra = set(fm) - ALLOWED_KEYS
    if extra:
        err(f"{rel}: frontmatter keys not accepted by claude.ai upload: {sorted(extra)}")
    name = fm.get("name", "")
    if not re.match(r"^[a-z0-9-]{1,64}$", name):
        err(f"{rel}: name must be 1-64 chars of lowercase letters, digits, hyphens")
    if name != skill.parent.name:
        err(f"{rel}: name '{name}' must match folder '{skill.parent.name}'")
    desc = fm.get("description", "")
    if not desc:
        err(f"{rel}: description is required")
    elif len(desc) > 1024:
        err(f"{rel}: description is {len(desc)} chars (keep it to 1024 or fewer)")

# 4. Declarative-agent instructions stay in sync.
src = ROOT / "microsoft/agent-instructions.md"
copy = ROOT / "microsoft/declarative-agent/appPackage/instruction.txt"
if src.exists() and copy.exists() and src.read_bytes() != copy.read_bytes():
    err("microsoft/declarative-agent/appPackage/instruction.txt differs from microsoft/agent-instructions.md (copy it across)")
if src.exists() and len(src.read_text(encoding="utf-8")) > 8000:
    err("microsoft/agent-instructions.md is over 8000 characters (Copilot instruction limit)")

# 5. Tool names referenced exist.
known = {
    line.strip()
    for line in (ROOT / "scripts/known-tools.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
}
TOOL_RE = re.compile(
    r"\b((?:create|add|update|delete|list|get|search|publish|discard|archive|unarchive|move|"
    r"reorder|rename|switch|merge|apply|finalize)_[a-z_]+)\b"
)
docs = skill_files + [src, ROOT / "AGENTS.md", ROOT / "docs/troubleshooting.md"]
for doc in docs:
    for tool in sorted(set(TOOL_RE.findall(doc.read_text(encoding="utf-8")))):
        if tool not in known:
            err(f"{doc.relative_to(ROOT)}: mentions unknown tool '{tool}'")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {len(skill_files)} skills, {len(known)} known tools.")
