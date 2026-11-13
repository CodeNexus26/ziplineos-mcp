# Changelog

All notable changes to this repository are recorded here. Dates are in AEST/AEDT.

## [Unreleased]

### Changed

- Synced with the ZiplineOS server as of 14 Nov 2026 (ziplineos#3977, #4000, #4113, #4212, #4332,
  #4362, #4369). Needs the ZiplineOS release that includes them.
  - Modules: a `Subject` item is now a **module**, a named group of forms on one step that people
    switch on or off for each deal in ZiplineOS (create-deal wizard, or the deal's workflow view).
    `subject.defaultIncluded: false` makes new deals start with it off. Switching on offers the new
    `moduleAdded` email; switching off clears the module's answers and is refused once the module
    is complete. The connector can't switch a module for a deal. The "Workflow Item: Subject"
    permission is now on by default. New skill `build-a-module`.
  - New skill `choose-scope-and-entries`: `scope` Shared or PerApplicant, `applicableRoles`,
    `minInstances` / `maxInstances`, and repeating groups.
  - New skill `tag-questions-for-the-form-filler` and documented tools `list_question_tags`,
    `set_question_tags`, `delete_question_tag`, `list_data_points` and `get_profile_coverage`.
  - Documented tools `add_applicant_role`, `update_applicant_role`, `delete_applicant_role`,
    `get_workflow_emails` and `update_workflow_email` (five emails, including `moduleAdded`; not
    versioned, so a change reaches every deal's next send at once).
  - Documented `get_guide` (the server's own guides) and `report_capability_gap`.
  - Rules: `notEquals` / `notContains` are true when there is no answer; `equals` / `notEquals`
    compare two numbers as numbers; a hidden item's or step's answers read as no answer.
  - `edit-a-published-workflow` lists what skips the Release Candidate: workflow emails, and forms,
    roles and item ownership on a never-published workflow.
  - The SuperAdmin-only deal tools (`create_deal`, `get_deal`, `list_deals`, `list_team_members`)
    are hidden from other accounts and stay undocumented.
- Release-Candidate-only editing (merge only after the matching ZiplineOS release is deployed to
  production).
  - Workflow-structure tools now edit only a workflow's Release Candidate, on a Draft or Published
    workflow. Since ZiplineOS publish gating, the Release Candidate reaches only test and preview
    deals; live deals run their published version until someone publishes the workflow in
    ZiplineOS.
  - Removed tools: `create_draft`, `list_drafts`, `get_draft`, `rename_draft`, `delete_draft`,
    `switch_editor_context`, `merge_draft_into_rc`, `get_merge_conflicts`,
    `apply_conflict_resolutions`, `finalize_merge`, `discard_release_candidate` and
    `publish_engine`. Drafts, merging and publishing a workflow or a calculation engine are done in
    ZiplineOS.
  - New refusals: "Workflow '…' has a draft loaded in its editor" (switch the editor back to the
    Release Candidate in ZiplineOS) and "Workflow '…' is Archived". The old "Published with no
    draft loaded" error, the live-deal guard and the "Draft workflow with no live deals" limit on
    triggers and delays are gone. Test and preview deals still run triggers.
  - `publish_form` makes form changes visible to test and preview deals at once; live deals get
    them when the workflow is next published in ZiplineOS.
  - Rewrote `edit-a-published-workflow`; updated `build-a-workflow`, `build-a-calculation-engine`,
    `form-field-conventions`, the paste-in instructions, `AGENTS.md`, README, `llms.txt`, client
    descriptions, troubleshooting and `scripts/known-tools.txt`.
- Org settings tools (ziplineos#3813). Needs the ZiplineOS release that includes it.
  - New tools: `get_branding`, `update_branding`, `get_document_ai_settings`,
    `update_document_ai_settings`, `add_document_category`, `update_document_category` and
    `delete_document_category`. They act on the user's own organisation only and need the Owner or
    Admin role. The document tools also need the AI Document Settings (`drive_ai`) permission.
  - `update_branding` sets the brand colour (`#RRGGBB`) and logos (https URL only) and returns
    `advice` on logo tone, plates, a needed alternate logo and contrast. Changes are recorded in
    the audit log.
  - New skill `set-up-branding-and-documents`; the paste-in instructions, README, AGENTS.md and
    llms.txt mention the tools. Skills say to confirm first.
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
