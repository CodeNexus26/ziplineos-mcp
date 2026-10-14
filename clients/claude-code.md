# Connect Claude Code

*Last verified: 2026-10-14.*

## Add the server

```bash
claude mcp add --transport http --client-id TODO(prod-client-id) \
  ziplineos https://api.ziplineos.com.au/api/v1/mcp
```
<!-- TODO(liam): replace with the production Claude Code client ID. After ZiplineOS supports
Client ID Metadata Documents, drop --client-id (Claude Code discovers it automatically). -->

Then, in Claude Code, run `/mcp`, select **ziplineos**, and sign in. Your browser opens the ZiplineOS
sign-in and consent screen. The consent screen warns that sign-in returns to an app on your
computer. That's expected for Claude Code, but only approve it if you started it yourself just
now.

Add `--scope project` to share the server with a project through `.mcp.json`, or leave it out to
add it for just yourself.

## Add the skills

Copy the skill folders into your personal skills directory:

```bash
git clone https://github.com/CodeNexus26/ziplineos-mcp.git
mkdir -p ~/.claude/skills
cp -R ziplineos-mcp/plugins/ziplineos/skills/* ~/.claude/skills/
```

## Plugin (server and skills in one step)

> **Status: coming soon.** The plugin needs ZiplineOS to support Client ID Metadata Documents, so
> that Claude Code can sign in without a client ID. Until then, use the two steps above.

```
/plugin marketplace add CodeNexus26/ziplineos-mcp
/plugin install ziplineos@ziplineos-mcp
```

After installing, run `/mcp` and sign in to the ZiplineOS server provided by the plugin.

## Check it works

Ask: *"Using ZiplineOS, list my workflows."* Claude should call `list_workflows` and show
the results.

If tools seem out of date after a ZiplineOS update, run `/mcp` and reconnect, or restart Claude
Code. See [docs/troubleshooting.md](../docs/troubleshooting.md).
