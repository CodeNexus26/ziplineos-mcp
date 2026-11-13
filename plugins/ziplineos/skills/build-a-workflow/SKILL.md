---
name: build-a-workflow
description: End-to-end recipe for building a NEW ZiplineOS workflow (stages, applicant roles, forms, checklists, documents, modules) with the ZiplineOS MCP tools, in the right order — forms first, publish them, then the workflow, roles, steps and items. Use when a user asks to create, set up or scaffold a new workflow, pipeline, process or fact find in ZiplineOS, or to add steps or items to a workflow that is still in Draft.
---

# Build a new ZiplineOS workflow

A **workflow** is the process a deal moves through. It has ordered **steps** (stages), and each
step holds **items**: forms the client or broker fills in, checklists, documents and
automations. Forms are separate objects that items link to.

Read the `form-field-conventions` skill before adding fields. If the connector offers `get_guide`,
call it with no name to see the server's own guides; they always match the current tools.

## 0. Plan with the user first

Before calling any write tool, write the plan out in plain language and get a yes:

- Workflow name and purpose.
- Steps in order, and which are end states (won / lost).
- For each step, its items: which forms (and their main questions), checklists, documents.
- Anything you will reuse. Check `list_workflows(nameQuery)` and `list_forms(nameQuery)` for an
  existing workflow or form with the same purpose. Reusing a form is usually better than making
  a near-duplicate.

## 1. Build and publish the forms

A workflow `Form` item can only link a **published** form, so forms come first.

1. `create_form_with_fields(name, description, fields)` creates the form and all its fields in
   one call, in array order. Bad field specs (unknown `configJson` key, bad visibility operator)
   are rejected before anything is created. If it fails part-way for some other reason, the form
   and the earlier fields already exist: `get_form` to see what landed, and continue with
   `add_field` rather than creating a second form.
   - For one or two fields on an existing form, use `add_field`.
2. Re-read with `get_form` and check keys, types, order and rules.
3. `publish_form(formTemplateId)`. A brand-new form isn't used by any live deal yet, but still
   tell the user you're publishing it. Publishing an existing form that deals already use needs
   their explicit yes (see `form-field-conventions`).

## 2. Create the workflow

`create_workflow(name, description?, icon?, color?)` creates it in **Draft**, with **one default
step** and a default **Primary Applicant** role.

- Call `get_workflow` straight away. Rename or reuse the default first step with `update_step`
  instead of leaving an empty extra step at the top.
- Only pass `icon` if you know the name is valid in ZiplineOS (e.g. `Home`); otherwise omit it.

## 2a. Set up the applicant roles

Add the roles the deal needs (Co-Applicant, Guarantor, ...) with `add_applicant_role`, and adjust
the default one with `update_applicant_role` (a PATCH). Do this before adding items, which name
roles. `list_workflow_roles` shows them.

- The first role is the primary role and holds one person only.
- `minCount` is how many people the role needs on a deal; `maxCount` is the most it can hold
  (omit for no limit; `clearMaxCount: true` removes one).
- `sharedSectionAccess` (`Hidden`, `View`, `Edit`) and `otherApplicantsSectionAccess` (`Hidden`,
  `View`) set what people in the role see in Collect. The primary applicant can always edit shared
  sections and add people.
- `delete_applicant_role` is refused while a Form item is filled by the role or an item still
  emails or texts it. Ask the user before deleting.

## 3. Add the steps

`add_step(workflowTemplateId, name, description?, color?, isTerminal, stageType)`

- `stageType`: `Normal` for ordinary stages; `Won` / `Lost` for end states (with
  `isTerminal: true`); `Lead` for an intake stage. Deals in a `Lead` stage are hidden from regular
  members until they move on, so only use `Lead` when the user wants that.
- Steps are appended. Fix the order at the end with `reorder_steps`, passing **every** step id in
  the new order.
- `update_step` is a PATCH: pass only what changes. Pass `""` to clear description or colour.

## 4. Add the items

`add_item(workflowTemplateId, stepId, name, type, ...)`. Supported `type`s and what each needs:

| type | Required | Notes |
|---|---|---|
| `Form` | `formTemplateId` of a **published** form | `applicantRoleId` is optional; get ids from `list_workflow_roles`. Set `scope` and entries (below). |
| `Checklist` | `checklistJson` | Array of `{"id":"…","text":"…","sortOrder":0,"children":[…]}`. Use short unique string ids. |
| `LiveDocument` | `workflowDocumentId` | Pick from `list_workflow_documents`. The connector can't upload documents; if the PDF isn't there, ask the user to upload it in ZiplineOS. Optional `autoFinalizeOnStepExit`. |
| `Integration` | `integration` (typed) | Pick `extensionSlug` from `list_integration_providers` (only installed providers work). Map inputs with `fieldMappings` to forms on this workflow. **Webhooks aren't supported.** An Equifax run is a paid credit enquiry, so confirm with the user before adding one. |
| `Subject` (a **module**) | `subject` (typed) | A named group of Form items on the same step that can be switched on or off per deal. Read the `build-a-module` skill first. |
| `Action` | `action` (typed) | `type` is `sendEmail`, `sendSms`, `addNote` or `cancelScheduledItems`. Recipients are `{kind, id}` with kind `applicantRole` or `teamRole`, from `list_workflow_roles` (a team role's id is its `memberTypeId`). Extra email addresses go in `cc`/`bcc`; SMS can take a custom phone number (`{kind:"custom", address}`). Only build from details the user gives you. `get_item` never shows stored custom addresses: a custom recipient comes back as `addressWithheld: true` with a `withheldRef` (`custom:1`), and stored cc/bcc addresses come back as refs (`cc:1`, `bcc:1`) with `ccWithheldCount` / `bccWithheldCount`. |

- **Who fills it and how many entries.** For Form, Checklist and LiveDocument items set `scope`:
  `Shared` (once for the deal) or `PerApplicant` (once per applicant; `applicableRoles` limits it
  to some roles). For Form and Checklist items set `minInstances` / `maxInstances` (`maxInstances`
  0 = no limit, e.g. one entry per property). When it isn't obvious, read the
  `choose-scope-and-entries` skill and ask the user.
- **Optional groups of forms.** When some deals need a set of forms and others don't, or the
  client gets them later, build a **module** (`Subject` item) instead of show/hide rules. New
  deals start with it on or off (`defaultIncluded`), and the advisor switches it per deal in
  ZiplineOS. See `build-a-module`.
- Items are appended to the step. Fix order with `reorder_items` (the **full** list of the step's
  item ids) or `move_item` (zero-based `targetIndex`, can move between steps).
- `update_item` changes only the attributes you pass (null = unchanged): name, `isRequired`,
  `isInternalOnly`, and the typed `action` / `integration` (fields you pass replace the stored
  ones; changing the action type or provider replaces the whole config). Read the current state
  first with `get_item`. Set rules with `set_item_rules` / `set_step_rules`.
  - **Withheld recipients and cc/bcc.** Leave `recipients`, `cc` or `bcc` out of the patch to keep
    them exactly as stored. If you do send one of those lists, it replaces the stored list, so
    echo what you want to keep by ref: `{"kind":"custom","withheldRef":"custom:1"}` for a custom
    recipient, `"cc:1"` / `"bcc:2"` for a cc/bcc address. Any patch that uses a ref must also pass
    the `configStamp` that `get_item` returned. If the item changed since you read it, the patch is
    refused: call `get_item` again and use the new refs and stamp. `cc: []` (or `bcc: []`) removes
    them all. A custom recipient sent with neither an address nor a `withheldRef` is refused, and
    so is a non-empty cc/bcc list with no refs while stored addresses exist (include the refs, or
    clear with `[]` first). Never guess or ask the user to repeat a withheld address just to keep it.
  - Don't use the raw `actionConfig` to edit an existing action: it replaces the whole config and
    drops any withheld recipient or cc/bcc address it doesn't spell out. Use the typed `action`.
  - Integration items: `get_item` hides some stored values. Keys the provider declares but whose
    names look personal or secret (e.g. `dateOfBirth`) are listed under `sensitiveParameterKeys` /
    `sensitiveInputKeys`; keys the provider doesn't declare are listed under
    `undeclaredParameterKeys` / `undeclaredInputKeys`. A typed `integration` patch keeps all of
    them even when you send `parameters` / `inputValues`; drop one only with `removeParameterKeys`
    / `removeInputKeys`, and only when the user asks.
- `resultsDisplay` (Integration items): `{preset, fieldNames?}` picks the result card staff and the
  client see. `default` shows label/value rows and needs `fieldNames` (deal custom-field keys; on a
  calc-engine item each must be one of the engine's visible outputs). `quote-estimate` and
  `repayment-savings` take no `fieldNames` and read fixed keys listed in the tool description (on a
  calc-engine item those keys must be engine outputs). Other presets aren't supported.
  `update_item` with `clearResultsDisplay: true` removes it.
- `assignedRoleId`: a team role (a `memberTypeId` from `teamRoles` in `list_workflow_roles`) saying
  who the item is for. It filters team views. An item has an applicant role or a team role, not
  both. `update_item` with `clearAssignedRole: true` removes it.
- To check a calc-engine Integration item, use `test_integration(workflowTemplateId, itemId,
  answers)`. Each answer is `{formTemplateId, fieldKey, value}` for a field the item maps (see
  `get_item` `fieldMappings`). It runs once, with no deal, and saves nothing. Paid providers never
  run, and other providers are refused.
- Action and Integration items only run on their own once they have an execution trigger
  (`executionTrigger`: `onStepEnter`, `onStepExit`, `onStepView` or `onItemView`) and, optionally,
  a `delay`. Confirm with the user before adding a trigger: the connector edits the Release
  Candidate, and test and preview deals **do** run triggers, so a trigger fires on those deals
  straight away. `onStepView` / `onItemView` fire on every view (the connector refuses them on
  integrations and email/SMS actions), and an Equifax run is a paid enquiry. A delay applies only
  to deals that enter the step after it is set. Switching a trigger to manual removes any delay,
  but clearing a trigger or delay doesn't cancel runs already scheduled: they still go ahead.

## 5. Word the emails (optional)

`get_workflow_emails` shows the workflow's five built-in emails (`invite`, `signingRequest`,
`signingCompletion`, `documentRequest` and `moduleAdded`, sent when an advisor switches a module
on) and the `{{tokens}}` each may use. `update_workflow_email` changes one. These emails **aren't
versioned**: a change reaches every deal's next send straight away, live deals included. Show the
user the wording and get a yes first.

## 6. Verify and hand over

1. `get_workflow` and compare against the agreed plan: step order, stage types, every item on
   the right step, every form item showing its form name.
2. Summarise what you built for the user.
3. **The connector cannot publish a workflow.** The workflow stays in Draft until someone
   publishes it in ZiplineOS. Tell the user that, and suggest they open it there to review it
   first.

## Errors you may see

Refusals say why (the validation reason, the allowed values, "must list every item exactly once").
Read the message and fix the call. Don't retry it unchanged.

- *"Workflow '…' has a draft loaded in its editor"*: someone has a draft open in the ZiplineOS
  workflow editor. The connector edits only the Release Candidate. Don't retry; ask the user to
  switch the editor back to the Release Candidate in ZiplineOS (see `edit-a-published-workflow`).
- *"Workflow '…' is Archived"*: unarchive it in ZiplineOS before editing.
- *"Item was not created … any linked form is published"*: publish the form first, or check the
  ids.
- To remove a workflow you created by mistake, use `delete_workflow(workflowTemplateId)`. It only
  works on a Draft workflow with no deals at all (test deals count). Ask the user first. Published
  or used workflows are refused: the user deletes those in ZiplineOS.
- *"Item type '…' is not supported yet"*: only the six types above are available.
- A `Subject` item refused with a permission error: the user's role lacks "Workflow Item:
  Subject". An admin turns it on in ZiplineOS. Don't build a stand-in (see `build-a-module`).
