# Security

## Reporting a vulnerability

Please **don't** open a public GitHub issue for security problems.

<!-- TODO(liam): choose the reporting channel (e.g. a security@ address, and/or enable GitHub
private vulnerability reporting on this repo) and fill it in below. -->
Report it privately to: `TODO(security-contact)`

Include what you found, how to reproduce it, and the impact you think it has. We'll acknowledge your
report and keep you updated while we investigate. Please give us reasonable time to fix the
problem before you disclose it.

This repository contains documentation and configuration only. Issues with the ZiplineOS service
itself (including the MCP server and its sign-in) should be reported through the same channel.

## What connecting an AI tool means

- **Sign-in and consent.** Connecting sends you to ZiplineOS to sign in. The consent screen shows
  the organisation and explains that approving lets the app act in ZiplineOS **as you, using
  your access**, for a limited time. Only approve if you started the connection yourself. If the
  screen says sign-in returns to an app on your computer and you didn't just start one (for example
  Claude Code), choose **Deny**.
- **Scope.** The connector requests the `mcp:workflows` scope. The MCP server only provides
  tools for building and editing workflows and forms in your own organisation. It doesn't
  provide tools for deals, contacts, documents or messages.
- **Your permissions apply.** The assistant can only see and change what your ZiplineOS account
  can. Each person connects with their own account.
- **Confirmation prompts.** Every tool is labelled as read-only, additive or destructive, so your
  AI client can ask you before it changes or removes anything. Clients differ in how they use
  these labels. Read what the assistant plans to do before you approve it.
- **Data sent to your AI provider.** What the tools return (workflow, form and question names,
  settings and rules) goes to the AI provider you connected, such as Anthropic, Microsoft or
  OpenAI, and is handled under your agreement with them. Don't connect a provider your
  organisation hasn't approved.

## Disconnecting

- **In ZiplineOS:** open your **personal settings → Connected AI apps** and revoke the app. The
  app can't renew its access after that. A session it already holds may keep working until it
  expires a short time later.
- **In the AI tool:** remove the ZiplineOS connector or MCP server too.
- **Microsoft Copilot (organisation-wide):** a ZiplineOS admin can revoke the organisation's
  Microsoft credentials, which disconnects everyone using that agent.

If you think a connection was misused, revoke it straight away and contact us using the channel
above.

## In this repository

- No secrets, tokens or client secrets are stored here. The only identifiers are public OAuth
  client IDs, which aren't secret.
- Never commit a client secret from the Microsoft Copilot setup to any repository.
