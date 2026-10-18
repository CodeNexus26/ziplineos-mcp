# ZiplineOS for AI assistants

Connect your AI assistant to **ZiplineOS** so it can build and maintain your workflows and forms
for you, in plain English.

> **Status: preview.** The ZiplineOS MCP connector has to be switched on for your organisation
> before any of this works. If you're not sure whether it is, ask your ZiplineOS administrator.

## What it is

ZiplineOS runs a remote [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server.
An AI assistant that supports MCP can sign in **as you** and use ZiplineOS tools to:

- find workflows, forms and questions by name;
- create forms and add, edit, reorder, show/hide or remove questions;
- create workflows and add or rearrange stages and items (forms, checklists, documents);
- change a live workflow safely through a draft, merging the changes into the next version, with
  you confirming any conflicts;
- where your organisation has it switched on, build, test and publish Logic calculation engines.

It **can't** publish a workflow to live deals; you do that in ZiplineOS. It can publish a
calculation engine, but only after you say yes. It can only see and change what
your own ZiplineOS account can, in your own organisation. It doesn't read or change deals, contacts or
client data, and it withholds the extra email addresses and phone numbers stored as recipients
(including cc and bcc) on workflow emails and texts.

**Who it's for:** brokers, practice managers and operations staff who set up workflows and fact
finds in ZiplineOS, and the IT admins who connect AI tools for them.

## Server URL

```
https://api.ziplineos.com.au/api/v1/mcp
```

Transport: Streamable HTTP. Auth: OAuth 2.1 with PKCE. You sign in to ZiplineOS and approve
access on a consent screen. There is nothing to install.

## Pick your AI tool

| Tool | Guide | Status |
|---|---|---|
| Claude (web, desktop, mobile) | [clients/claude.md](clients/claude.md) | Available |
| Claude Code | [clients/claude-code.md](clients/claude-code.md) | Available (plugin coming soon) |
| Microsoft Copilot (Copilot Studio, Microsoft 365 Copilot) | [clients/microsoft-copilot.md](clients/microsoft-copilot.md) | Coming soon |
| ChatGPT | [clients/chatgpt.md](clients/chatgpt.md) | Coming soon |
| Other MCP clients | [clients/other.md](clients/other.md) | Best effort |

## Get better results: skills

Connecting gives your AI the tools. The **skills** in this repo teach it how to use them well:
the right order to build a workflow, how not to overwrite a question's settings, and when to
stop and ask you before anything goes live.

| Skill | Teaches |
|---|---|
| [build-a-workflow](plugins/ziplineos/skills/build-a-workflow/SKILL.md) | Building a new workflow end to end |
| [edit-a-published-workflow](plugins/ziplineos/skills/edit-a-published-workflow/SKILL.md) | Draft → merge → resolve conflicts, and editing forms that are in use |
| [form-field-conventions](plugins/ziplineos/skills/form-field-conventions/SKILL.md) | Keys, types, ordering, show/hide rules, money fields, safe edits |
| [fact-find-patterns](plugins/ziplineos/skills/fact-find-patterns/SKILL.md) | Common shapes for Australian mortgage fact finds |
| [build-a-calculation-engine](plugins/ziplineos/skills/build-a-calculation-engine/SKILL.md) | Building, testing and publishing a Logic calculation engine |

Each client guide explains how to load them. For Microsoft Copilot and ChatGPT, paste
[microsoft/agent-instructions.md](microsoft/agent-instructions.md) into the agent's instructions.

Not sure what to ask first? See [prompts/](prompts/).

## Your data and your control

- The assistant acts with **your** ZiplineOS permissions, in your organisation only.
- Information the tools return (workflow, form and question names and settings) is sent to the AI
  provider you connect (for example Anthropic, Microsoft or OpenAI) and handled under that
  provider's terms.
- You can disconnect any time in ZiplineOS: **personal settings → Security → Connected AI apps**.
- Assistants ask before risky actions, but **read what they plan to do before you approve it.**

See [SECURITY.md](SECURITY.md) for scopes, consent and how to report a security issue.

## For AI agents

If you are an AI agent asked to "set up ZiplineOS", follow [AGENTS.md](AGENTS.md). A
machine-readable index is in [llms.txt](llms.txt).

## Help

- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Support: <!-- TODO(liam): public support contact (email or help-centre URL). -->contact ZiplineOS support.

## Licence

See [LICENSE](LICENSE).
