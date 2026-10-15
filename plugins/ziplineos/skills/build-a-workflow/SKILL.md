---
name: build-a-workflow
description: End-to-end recipe for building a NEW ZiplineOS workflow (stages, forms, checklists, documents) with the ZiplineOS MCP tools, in the right order — forms first, publish them, then the workflow, steps and items. Use when a user asks to create, set up or scaffold a new workflow, pipeline, process or fact find in ZiplineOS, or to add steps or items to a workflow that is still in Draft.
---

# Build a new ZiplineOS workflow

A **workflow** is the process a deal moves through. It has ordered **steps** (stages), and each
step holds **items**: forms the client or broker fills in, checklists, documents and
automations. Forms are separate objects that items link to.

Read the `form-field-conventions` skill before adding fields.

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
| `Form` | `formTemplateId` of a **published** form | `applicantRoleId` is optional; get ids from `list_workflow_roles`. |
| `Checklist` | `checklistJson` | Array of `{"id":"…","text":"…","sortOrder":0,"children":[…]}`. Use short unique string ids. |
| `LiveDocument` | `workflowDocumentId` | Pick from `list_workflow_documents`. The connector can't upload documents; if the PDF isn't there, ask the user to upload it in ZiplineOS. Optional `autoFinalizeOnStepExit`. |
| `Integration` | `integration` (typed) | Pick `extensionSlug` from `list_integration_providers` (only installed providers work). Map inputs with `fieldMappings` to forms on this workflow. **Webhooks aren't supported.** An Equifax run is a paid credit enquiry, so confirm with the user before adding one. |
| `Action` | `action` (typed) | `type` is `sendEmail`, `sendSms`, `addNote` or `cancelScheduledItems`. Recipients are role ids from `list_workflow_roles`; for extra email addresses use `cc`/`bcc`. Only build from details the user gives you. |

- Items are appended to the step. Fix order with `reorder_items` (the **full** list of the step's
  item ids) or `move_item` (zero-based `targetIndex`, can move between steps).
- `update_item` changes only the attributes you pass (null = unchanged): name, `isRequired`,
  `isInternalOnly`, and the typed `action` / `integration` (fields you pass replace the stored
  ones). Read the current state first with `get_item`. Set rules with `set_item_rules` /
  `set_step_rules`.
- Action and Integration items don't run on their own yet: they need an execution trigger, which
  the connector can't set. Tell the user to set the trigger in ZiplineOS, or run the item by hand
  from the deal.

## 5. Verify and hand over

1. `get_workflow` and compare against the agreed plan: step order, stage types, every item on
   the right step, every form item showing its form name.
2. Summarise what you built for the user.
3. **The connector cannot publish a workflow.** The workflow stays in Draft until someone
   publishes it in ZiplineOS. Tell the user that, and suggest they open it there to review it
   first.

## Errors you may see

- *"Workflow '…' is Published with no draft loaded"*: you're trying to change a live workflow.
  Stop and follow the `edit-a-published-workflow` skill.
- *"Item was not created … any linked form is published"*: publish the form first, or check the
  ids.
- *"Item type '…' is not supported yet"*: only the five types above are available.
