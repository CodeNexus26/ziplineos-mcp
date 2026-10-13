# Other MCP clients

**Status: best effort.** Any MCP client that supports **Streamable HTTP** and **OAuth 2.1 with
PKCE** may work. Point it at:

```
https://api.ziplineos.com.au/api/v1/mcp
```

The server publishes standard OAuth discovery documents (protected-resource metadata and
authorisation-server metadata), so a compliant client can find the sign-in endpoints from the
URL. The OAuth scope is `mcp:workflows`.

> ZiplineOS doesn't support Dynamic Client Registration. It currently accepts only clients it
> already knows. Support for Client ID Metadata Documents, the method the MCP specification now
> prefers, is planned. Until then, most clients that aren't listed in this repository won't be
> able to sign in.

## Gemini CLI

> **Status: coming soon** (needs Client ID Metadata Document support).

```json
// ~/.gemini/settings.json
{ "mcpServers": { "ziplineos": { "httpUrl": "https://api.ziplineos.com.au/api/v1/mcp" } } }
```

Then run `/mcp auth ziplineos`.

## Instructions for any assistant

Paste [`microsoft/agent-instructions.md`](../microsoft/agent-instructions.md) into your
assistant's system or project instructions so it follows the safe editing rules.
