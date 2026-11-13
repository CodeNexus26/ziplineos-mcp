---
name: build-a-module
description: How to build a module in a ZiplineOS workflow with the ZiplineOS MCP tools. A module is a named group of forms on one step (a "Subject" item in the tools) that works like a small workflow inside the main one and can be switched on or off for each deal. Covers when to use one, defaultIncluded (on or off for new deals), the order of work, completion and visibility, delegation reminders, the "module added" email, and changing a module safely. Use when a user asks for optional sections, add-on questionnaires, forms only some clients get, forms sent later, or a group of forms for one policy, product, property or renewal.
---

# Build a module

A **module** is a named group of forms on one workflow step that ZiplineOS can **switch on or off
for each deal**. Think of it as a small workflow inside the main one: a health questionnaire, a
risk-tolerance questionnaire, a motor policy (vehicle + drivers + claims history). The client sees
the module as one heading with its forms inside it, in Collect and on the deal.

In the tools a module is an item of type **`Subject`**. Users see the word "module" in ZiplineOS.
Use "module" with the user.

The server's own guide (`get_guide` with name `build-a-subject`) has the latest detail. Read it
when the connector offers it.

## When to use one

- **Forms only some deals need, or need later.** For example, a financial planning workflow with
  client information, a health questionnaire and a risk-tolerance questionnaire. Some clients do
  all three at once; others get only one now and the rest later. Make each optional set a
  module and the advisor switches it on per deal. No show/hide rules needed.
- **Several forms that describe one thing** and should read as one unit: a policy, a product, a
  property, a renewal.
- **Not** for a single form that repeats (one entry per property): use `maxInstances` on that Form
  item. **Not** for something each applicant fills: use scope PerApplicant. See the
  `choose-scope-and-entries` skill. If unsure which the user means, ask.
- Don't use show/hide rules on a creation-form field to fake a module. That's the fragile setup
  modules replace.

## How switching works on a deal

You set the default; people switch modules on the deal in ZiplineOS. The connector has no tool to
switch a module on or off for a deal. Tell the user how it works:

- **New deals** start with each module on or off according to its `defaultIncluded`. In the manual
  create-deal wizard the advisor can change the selection on a **Modules** step. Every other way a
  deal is created (self-registration link, import, duplicate, automation) uses the defaults.
- **On an existing deal** anyone who can edit the deal can switch a module on or off from the
  deal's workflow view.
- **Switching on** offers the workflow's **module added** email to the client (edit, then Send or
  Don't send). The client sees the module the next time they open Collect.
- **Switching off** is allowed only until the module is complete, and **clears the client's
  answers** to its forms (ZiplineOS asks the advisor to confirm). A completed module is locked on.
- **Off means hidden everywhere** the client looks, and the module's forms don't count towards
  step completion. Staff still see it on the deal, greyed out.
- **Switched on after the deal has moved past its step:** the deal doesn't move back. The client
  completes it in Collect, the deal card shows "modules outstanding", and the earlier step's exit
  actions don't run again.
- **A deal can't be marked Won** while an included module has unfinished required forms.

## Before you start: the permission

Building a module needs the organisation's **Workflow Item: Subject** permission (`item_subject`).
It's on by default for Owners, Admins and Members, but an organisation can turn it off for a role.

- If `add_item` with type `Subject` (or `update_item` with `subject`) is refused with a permission
  error, stop. Tell the user an admin must turn on "Workflow Item: Subject" for their role in
  ZiplineOS. Don't build a stand-in from plain forms and rules, and don't pretend it's the same.
- The member forms and their Form items don't need the permission. You can build them first.
- Reading a module (`get_item`, `get_workflow`) needs no extra permission.

## Order of work

1. **Plan the module with the user.** Agree its name (the label clients see, e.g. "Health
   questionnaire" or "Policy"), which forms make it up, in what order, and whether new deals start
   with it **on or off**.
2. **Build and publish the member forms** with `create_form_with_fields`, then `publish_form` (ask
   first). If one question's answer names each one (a rego, a policy number), note its key.
3. **Add the member Form items to ONE step** with `add_item` (type `Form`). Every member must be on
   the module's own step; a member on another step never appears inside it. Set each member's
   required flag, scope and rules on the member.
4. **Add the module on that same step** with `add_item`, type `Subject`, and `subject`:
   - `memberItemIds`: the member Form item ids, in display order. At least one. A form can belong
     to one module only, and the module can't list itself or a non-Form item.
   - `displayLabel`: the noun clients see. Leave it out to use the item name.
   - `defaultIncluded`: `false` makes new deals start with the module **off** (switched on per
     deal). Leave it out, or `true`, for on.
   - `instanceLabelFieldKey`: optional key of a question on a member form whose answer names each
     one. It's stored but not shown to clients yet; don't promise that it will be.
   - `reminders`: optional delegation reminder schedule (below). Leave it out for the standard one.
5. **Word the module added email** if the user wants: `get_workflow_emails`, then
   `update_workflow_email` with `emailType: "moduleAdded"`. Email changes aren't versioned and
   reach every deal's next send straight away, so confirm the wording first.
6. **Read it back** with `get_item` on the module. Check every member is listed by name with no
   `missing: true`, `clientLabel` is right, and `defaultIncluded` is what the user chose.

## Completion and visibility

- **Member forms carry completion.** The module item itself counts as complete. To make part of a
  module optional, make those member forms optional.
- **Member forms carry their own rules.** When the module is on, each member's show/hide rules
  still apply. The module switch is an extra condition, not a replacement for rules.
- A module item accepts showWhen / hideWhen only (`set_item_rules`), and takes no scope or entry
  counts. Prefer the per-deal switch over rules on the module.

## Delegation reminders

In Collect a client may hand a module to someone else to fill in. The reminder schedule decides
how often that person is emailed:

- Standard schedule: 2 and 5 days after the invite, and 1 day before the link expires.
- `reminders: {enabled, offsetDays, remindBeforeExpiry, beforeExpiryDays}`. `offsetDays` are days
  after the invite, each 1 or more, at most 10. `enabled: false` sends the invite and no
  reminders. `beforeExpiryDays` is at least 1.
- These emails go to people outside the organisation. Confirm the schedule with the user rather
  than inventing one. Out-of-range values are refused.
- In `update_item`, a `reminders` patch changes only what you send. `useDefaultReminders: true`
  goes back to the standard schedule.

## Changing a module

- `update_item` with `subject` patches. A supplied `memberItemIds` **replaces** the member list
  (send the whole list, in order). `displayLabel` or `instanceLabelFieldKey` set to `""` clears
  it. `defaultIncluded` changes only what **new** deals start with; existing deals keep their
  switches. Anything you leave out is kept.
- The module's PDF pack and its "offered when" condition are set only in the ZiplineOS item
  editor. `get_item` reports them as `pdfDocumentCount` and `hasRequiredIf`; `update_item` never
  changes them.
- To move a form between modules, first remove it from the old module, then add it to the new one.
- **Moving between steps ungroups.** If you `move_item` a member or the module, move the module and
  all its members together, then check `get_item` for `missing: true`.
- After deleting a member form's item, update the module's member list.
- `hasUnrecognisedSubjectConfig: true` means the stored config can't be read. Replace it with
  `update_item` and a full `memberItemIds` list, after confirming the members with the user.

## Where edits land

Like any structure edit, module changes land on the workflow's Release Candidate (test and preview
deals) and are refused while a draft is loaded in the ZiplineOS editor. Live deals get them once
the user publishes the workflow in ZiplineOS.
