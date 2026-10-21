# Changelog

All notable changes to this repository are recorded here. Dates are in AEST/AEDT.

## [Unreleased]

### Changed

- Synced with the ZiplineOS server as of 21 Oct 2026 (ziplineos#3753, #3759, #3793). Needs the
  ZiplineOS release that includes them.
  - New tools: `delete_workflow` (Draft workflow with no deals), `delete_engine` (never published,
    not used anywhere) and `test_integration` (runs a calc-engine Integration item once on sample
    answers; no deal, nothing saved). Skills and paste-in instructions say to ask first.
  - Calc engine Switch case keys match ignoring case; keys that differ only by case are refused at
    publish. A new engine's first publish is version 1. `delete_computation` / `delete_output`
    renumber the rest. Renaming an engine or editing its description marks it as having
    unpublished changes.
  - `resultsDisplay` on Integration items picks the result card (`default` with `fieldNames`,
    `quote-estimate`, `repayment-savings`). `update_item` `clearResultsDisplay` removes it.
  - `assignedRoleId` assigns an item to a team role (not with an applicant role).
    `clearAssignedRole` removes it. Neither change is blocked by the live-deal guard, so confirm
    first on a live workflow.
  - Refusals now say why. The skills tell the agent to read the message and fix the call.
  - Reactions are not advertised; the skills now say "automatic follow-ups set up in ZiplineOS".
- Synced with the ZiplineOS server as of 17 Oct 2026 (ziplineos#3689, #3696, #3706, #3708). Needs
  the ZiplineOS release that includes them.
  - `get_item` withholds custom recipient addresses (`addressWithheld` + `withheldRef`) and cc/bcc
    addresses (refs `cc:N` / `bcc:N`), and returns a `configStamp`. The skills and paste-in
    instructions explain keeping them by ref with the stamp, clearing with `[]`, and avoiding a raw
    `actionConfig` rewrite. Hidden integration keys are listed under `sensitive*Keys` /
    `undeclared*Keys`.
  - `edit-a-published-workflow`: the live-deal guard. While a draft is loaded on a published
    workflow with live deals, edits that change what those deals run are refused. The skill says
    to stop, explain, and offer what still works (including merging a draft without loading it).
  - README, `AGENTS.md`, `SECURITY.md` and `llms.txt` mention the calculation engine tools.
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

- Skill `build-a-calculation-engine`: build → test → validate → publish for Logic Custom
  calculation engines, using the 18 engine tools (behind the `engine_ai_authoring` permission).
  `scripts/known-tools.txt` lists them, and `validate.py` now also checks `test_*` / `validate_*`
  tool names.

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
