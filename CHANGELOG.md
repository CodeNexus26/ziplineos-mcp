# Changelog

All notable changes to this repository are recorded here. Dates are in AEST/AEDT.

## [Unreleased]

### Changed

- Repository renamed to `ziplineos-mcp`.
- Skills and paste-in instructions: Action and Integration items use the connector's typed
  `action` / `integration` specs, with `list_workflow_roles` and `list_integration_providers` for
  lookups. Webhook integrations aren't supported, and an Equifax run must be confirmed first
  (paid). Rules use `set_item_rules` / `set_step_rules`. Execution triggers and delays can be set
  on Draft workflows with no live deals. Needs the matching ZiplineOS release.
- Licence: all rights reserved, with use permitted for ZiplineOS customers connecting their own
  assistants. Security reports go to `security@ziplineos.com.au`.
- `SECURITY.md`: the access token now works only on the MCP endpoint, and disconnecting ends
  access straight away (both verified on staging, 14 Oct 2026). Disconnect path is
  **personal settings → Security → Connected AI apps**.

### Added

- Setup guides for Claude (web, desktop, mobile), Claude Code, Microsoft Copilot (Copilot Studio
  and Microsoft 365 Copilot; coming soon), ChatGPT (coming soon) and other MCP clients.
- `AGENTS.md` and `llms.txt` for AI agents asked to set up ZiplineOS.
- Claude Code plugin `ziplineos` (MCP server and skills) and marketplace manifest.
- Skills: `build-a-workflow`, `edit-a-published-workflow`, `form-field-conventions`,
  `fact-find-patterns`.
- Paste-in agent instructions for Microsoft Copilot, ChatGPT and other assistants, and an
  illustrative Microsoft 365 declarative-agent sample.
- Starter prompts, troubleshooting guide, security policy.
- CI: Markdown lint, link check, manifest and skill-frontmatter validation, and a tool-name drift
  check.
