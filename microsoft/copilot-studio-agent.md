# Build the ZiplineOS agent in Copilot Studio

> **Status: coming soon.** See the status note in
> [clients/microsoft-copilot.md](../clients/microsoft-copilot.md). This walkthrough describes the
> intended setup.

*Last verified: 2026-10-14.*

<!-- TODO(liam): add screenshots for each step once the ZiplineOS admin wizard exists. -->

## 1. Generate credentials in ZiplineOS

ZiplineOS **Admin → AI connections → Microsoft Copilot → Generate credentials**. You get:

| Value | Where it goes in Copilot Studio |
|---|---|
| Client ID | OAuth 2.0 → Client ID |
| Client secret (shown once) | OAuth 2.0 → Client secret |
| Authorisation URL | Authorization URL |
| Token URL | Token URL |
| Refresh URL | Refresh URL |
| Scope | Scopes |

These credentials only work for **your** ZiplineOS organisation.

## 2. Create the agent

1. Copilot Studio → **Create** → **New agent**. Skip the conversational setup and configure it
   directly.
2. Name: `ZiplineOS`. Description: `Builds and edits ZiplineOS workflows and forms.`
3. **Instructions:** paste the contents of [agent-instructions.md](agent-instructions.md).
4. Optional starter prompts, from [prompts/](../prompts/):
   - *List my workflows and summarise the fact-find steps.*
   - *Find every question about income in the home loan fact find.*

## 3. Add ZiplineOS as an MCP tool

1. **Tools → Add a tool → New tool → Model Context Protocol.**
2. Server name `ZiplineOS`, description as above, server URL
   `https://api.ziplineos.com.au/api/v1/mcp`.
3. Authentication: **OAuth 2.0**, type **Manual**, and fill in the table from step 1.
4. **Create.** Copilot Studio shows a **redirect URL**. Paste it into the ZiplineOS credentials
   page and save. Sign-in fails until you do.

## 4. Connect and test

1. **Create new connection** → sign in to ZiplineOS → approve on the consent screen.
2. **Add to agent.**
3. In the **Test** pane, ask *"List my ZiplineOS workflows."*
4. Try one change on a test form and check that the agent asks before publishing.

## 5. Publish to the brokerage

1. **Publish**, then under **Channels** add **Microsoft Teams and Microsoft 365 Copilot**.
2. Make the agent available to the right users or groups (your tenant's approval process may
   apply).
3. Tell brokers to open the agent and sign in to ZiplineOS when prompted. Each broker's own
   ZiplineOS permissions apply.

## Maintenance

- **New ZiplineOS tools:** in the agent's **Tools**, refresh the MCP tool so Copilot picks up
  the new tool list.
- **Rotate the secret:** generate a new secret in ZiplineOS and update the connection.
- **Remove access:** revoke the credentials in ZiplineOS.
