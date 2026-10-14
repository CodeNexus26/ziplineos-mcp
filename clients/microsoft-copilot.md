# Connect Microsoft Copilot (Copilot Studio and Microsoft 365 Copilot)

> **Status: coming soon.** This guide shows the intended setup. It depends on two ZiplineOS
> features that aren't released yet: **organisation-specific Microsoft credentials**, created by
> your ZiplineOS admin, and **long-lived sign-in**, so Copilot doesn't ask brokers to sign in
> every few hours. Until they ship, Copilot can't connect to ZiplineOS.

*Last verified: 2026-10-14. Microsoft's menus change often. Look for the closest label, and
check Microsoft's own docs for
[Copilot Studio MCP](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
and [Microsoft 365 Copilot MCP plugins](https://learn.microsoft.com/microsoft-365/copilot/extensibility/build-mcp-plugins).*

**Who this is for:** your brokerage's **Microsoft 365 admin**, working with a **ZiplineOS
admin**. Brokers don't set anything up. They use the agent and sign in to ZiplineOS once.

**How it works:** you build a "ZiplineOS" agent once for the whole brokerage. Each broker who
uses it signs in with their own ZiplineOS account, so their own permissions apply.

## Before you start

- A ZiplineOS admin account in your organisation.
- Copilot Studio access in your Microsoft 365 tenant, with permission to publish agents to Teams
  and Microsoft 365 Copilot.
- The server URL: `https://api.ziplineos.com.au/api/v1/mcp`

## Path A: Copilot Studio agent (recommended)

1. **Create credentials in ZiplineOS.** Go to **Admin → AI connections → Microsoft Copilot →
   Generate credentials**. Copy the client ID, client secret, authorisation URL, token URL,
   refresh URL and scope. The secret is shown **once**, so store it somewhere safe.
2. **Create the agent.** In Copilot Studio, create an agent called `ZiplineOS`. Paste the text of
   [`microsoft/agent-instructions.md`](../microsoft/agent-instructions.md) into its
   **Instructions**.
3. **Add the MCP tool.** In the agent, go to **Tools → Add a tool → New tool → Model Context
   Protocol**. Enter:
   - Name: `ZiplineOS`
   - Description: `Build and edit ZiplineOS workflows and forms for this brokerage.`
   - Server URL: the URL above
   - Authentication: **OAuth 2.0 → Manual**, then paste the values from step 1.
   Choose **Create**.
4. **Register the redirect URL.** Copilot Studio shows a **redirect URL** for this connector.
   Copy it into the ZiplineOS credentials page and choose **Save**.
5. **Connect and test.** Create the connection (sign in to ZiplineOS and approve), choose
   **Add to agent**, then **Test**. Ask *"List my ZiplineOS workflows."*
6. **Publish.** Publish the agent to **Microsoft Teams** and **Microsoft 365 Copilot**, and make it
   available to the right people. Each broker signs in to ZiplineOS the first time they use it.

A longer walkthrough is in [`microsoft/copilot-studio-agent.md`](../microsoft/copilot-studio-agent.md).

## Path B: Microsoft 365 Copilot declarative agent (Agents Toolkit)

For tenants that build agents in VS Code with the Microsoft 365 Agents Toolkit. MCP support
there is in **preview** and may change.

1. Create a new **declarative agent**, choose **Add action → Start with an MCP server**, and enter
   the server URL.
2. Choose the ZiplineOS tools to include.
3. Configure **OAuth** with the same credentials as Path A, step 1. Register the redirect URL
   the toolkit gives you in ZiplineOS.
4. Provision and test.

A starting sample is in [`microsoft/declarative-agent/`](../microsoft/declarative-agent/).

## Path C: approve ZiplineOS from Microsoft's catalogue

> Coming later. Once ZiplineOS is listed in Microsoft's agent catalogue, an admin can approve it
> in the Microsoft 365 admin centre, and brokers will find it ready to use.

## Notes

- Copilot Studio uses the **Streamable HTTP** MCP transport, which ZiplineOS supports.
- If the MCP option doesn't appear in your tenant, Microsoft may not have enabled it in your region
  yet. The fallback is a Power Apps **custom connector** with the same OAuth values.
- Copilot asks the user before running actions marked as changing or removing data. ZiplineOS
  labels every tool as read-only, additive or destructive, so these prompts are accurate.
- To rotate the client secret, generate a new one in ZiplineOS and update the connector. The old
  secret stays valid for a short overlap.
- To remove access for everyone, revoke the credentials in ZiplineOS. Individual brokers can
  disconnect under **personal settings → Security → Connected AI apps**.
