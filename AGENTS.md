# Instructions for AI agents

You have been asked to connect a user's AI tool to **ZiplineOS**, or to work with ZiplineOS
through it. Follow these steps in order. Don't invent settings that aren't in this repository.

## Facts

- MCP server URL: `https://api.ziplineos.com.au/api/v1/mcp`
- Transport: Streamable HTTP. Auth: OAuth 2.1 + PKCE (authorisation code). Scope: `mcp:workflows`.
- No Dynamic Client Registration. The client must be one ZiplineOS already recognises.
- The user signs in to ZiplineOS in a browser and approves a consent screen. **You can't do this
  for them.** Never ask for their password, and never type credentials for them.
- Tools only cover authoring workflows, forms and (where the organisation has it switched on)
  Logic calculation engines in the user's own organisation. `test_integration` runs a calculation
  integration on sample answers and saves nothing. For Owners and Admins, the org settings tools
  (`get_branding`, `update_branding`, the document AI settings and category tools) change the
  organisation's branding and AI document settings. The question-tag tools
  (`list_question_tags`, `set_question_tags`, `delete_question_tag`, `list_data_points`,
  `get_profile_coverage`) set up the ZiplineOS Chrome extension form filler.
- `get_guide` serves the server's own authoring guides, which always match the current tools.

## 1. Work out the client

Ask which AI tool they use, if it isn't obvious, then follow the matching guide:

| Client | Guide |
|---|---|
| Claude web / desktop / mobile | [clients/claude.md](clients/claude.md) |
| Claude Code | [clients/claude-code.md](clients/claude-code.md) |
| Microsoft Copilot Studio / Microsoft 365 Copilot | [clients/microsoft-copilot.md](clients/microsoft-copilot.md) |
| ChatGPT | [clients/chatgpt.md](clients/chatgpt.md) |
| Anything else | [clients/other.md](clients/other.md) |

If the guide starts with **Status: coming soon**, tell the user that the client can't connect
yet and stop. Don't try workarounds.

## 2. Connect

- **Claude Code (you can run commands):** run the `claude mcp add …` command from
  [clients/claude-code.md](clients/claude-code.md) exactly as written, then ask the user to run
  `/mcp` and complete sign-in in their browser.
- **Other clients:** give the user the numbered steps from the guide. You can't click through
  their settings for them unless they've given you a tool that can, and even then they must
  complete the ZiplineOS sign-in and consent themselves.

## 3. Install the skills

The skills in [`plugins/ziplineos/skills/`](plugins/ziplineos/skills/) contain the rules for
using the tools well. Install them the way the client guide describes. Where a client can't load
skills, use [microsoft/agent-instructions.md](microsoft/agent-instructions.md) as instructions.

## 4. Verify (read-only)

Call `list_workflows` with no filters. A list (even an empty one) means the connection works.
Don't call any tool that changes data as a test.

| Result | Meaning | Action |
|---|---|---|
| A list | Connected | Done. Suggest a prompt from [prompts/](prompts/README.md). |
| 401 / sign-in prompt | Not signed in, or the session expired | User reconnects and signs in. |
| 403 "connector is not enabled" | Not switched on for their environment or organisation | User contacts their ZiplineOS administrator. |
| Tool not found | Stale tool list | Remove and re-add the connector ([troubleshooting](docs/troubleshooting.md)). |

## 5. When you use the tools

Read the skills before you change anything, and call `get_guide` (no name lists the guides) for
the server's current guidance. The rules that matter most:

- Resolve workflows and forms **by name**. Never ask the user for ids.
- `update_field`, `update_step` and `update_item` change only what you pass. Never re-send
  unchanged attributes.
- Ask before changing a workflow email (`update_workflow_email` reaches every deal's next send at
  once, live deals included).
- Ask before publishing a form that is in use, archiving, deleting (`delete_workflow`,
  `delete_engine`, `delete_document_category`), changing branding or AI document settings, or
  discarding.
- Workflow-structure tools edit only the workflow's Release Candidate, which test and preview
  deals run. Live deals get it once a person publishes the workflow in ZiplineOS. Publishing a
  workflow or a calculation engine is done in ZiplineOS only.
- If a tool says the workflow "has a draft loaded in its editor", don't retry or work around it.
  Ask the user to switch the editor back to the Release Candidate in ZiplineOS (see the
  `edit-a-published-workflow` skill).
- A module is a `Subject` item: a group of forms on one step that people switch on or off per
  deal in ZiplineOS. No tool switches it for a deal; `defaultIncluded` sets how new deals start.
- If the user asks for something ZiplineOS can do but no tool can, call `report_capability_gap`
  with a generic description (never the user's data), then keep helping.
