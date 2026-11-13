---
name: choose-scope-and-entries
description: How to decide who fills a ZiplineOS workflow item and how many entries it takes, with the ZiplineOS MCP tools — scope Shared or PerApplicant (and applicableRoles), single or multiple entries (minInstances / maxInstances), and when a repeating group inside a form fits better. Use before add_item or update_item on a Form, Checklist or LiveDocument item, or when a user asks for something "per applicant", "for each property/employer/loan", "only for guarantors", or "they may have none".
---

# Choose scope and entries

Every Form, Checklist and LiveDocument item answers two questions:

1. **Who completes it?** `scope`: Shared (once for the whole deal) or PerApplicant (once for each
   applicant).
2. **How many entries?** (Form and Checklist only) `maxInstances` and `minInstances`: one entry, or
   several the person adds one by one.

Decide both before calling `add_item`, and ask the user when the answer isn't obvious. Getting it
wrong is costly. Answers end up in the wrong place, rules can't reach them, and changing it later
changes what live deals need.

## Shared or PerApplicant

Ask: **"Would two applicants on the same deal give different answers?"**

- **Different answers → PerApplicant.** Each applicant gets their own copy and their own answers.
  Typical: personal details, identification, employment and income, their own credit history
  consent, residency status, each person's assets and liabilities when they're held individually.
- **One answer for everyone → Shared.** One copy for the deal. Typical: loan purpose and amount,
  the security property, the deal's lender preferences, household expenses for a couple who share
  them, anything about the deal rather than a person.
- **Only some roles fill it** (e.g. a guarantor statement): PerApplicant plus `applicableRoles`
  with the role names from `list_workflow_roles`. Omitted or [] means every applicant. A Shared item
  can't be restricted to roles: it's filled once for the deal.
- **Not sure?** If the user thinks of the deal as "the couple" and the item as "theirs", ask whether
  each person might answer it differently, such as separate employers or separate debts. If they
  might, use PerApplicant.

Who can see and edit what in Collect is set on the applicant roles, not on the item.
`sharedSectionAccess` (Hidden, View, Edit) controls Shared items, and `otherApplicantsSectionAccess`
(Hidden, View) controls other applicants' PerApplicant items. The primary applicant can always edit
Shared items. If a co-applicant has to fill a Shared item, check their role has Edit
(`list_workflow_roles`, `update_applicant_role`).

There is no per-household option to choose here. For something a couple shares, use Shared.

## One entry or several

Ask: **"Could there be more than one of these?"**

- **Exactly one → single entry.** `maxInstances` 1, the default. Personal details, the loan
  request, a declaration.
- **Possibly several → multiple entries.** `maxInstances` greater than 1 for a real cap, or 0 for
  no limit. Each entry is a full copy of the form: one per property owned, employer (current and
  previous), vehicle, loan or credit card, dependant.
- `minInstances` is how many entries are needed. The default is 1. Use 0 when "none" is a valid
  answer (no other properties, no credit cards). It can't exceed a non-zero `maxInstances`.
- **Combine freely.** PerApplicant with several entries is common: each applicant lists their own
  employers. Shared with several entries fits deal-level lists, such as the securities on a deal.

### A multi-entry item, or a repeating group inside one form?

A form can also repeat a block of questions itself: a `NestedForm` field with `isRepeatable` (see the
`form-field-conventions` skill). Choose by size and weight:

- **Repeating group inside the form**: a few short questions per row, read as one list. Examples:
  dependants (name, age), previous addresses, other names used. One submission holds every row.
- **Multi-entry item**: each entry is substantial, like a property with its address, value, loan
  and rent. Each entry is reviewed or chased on its own, and the client adds them one at a time.
  Each entry is its own submission.

If one list keeps growing more questions per row, it's a multi-entry item. If each entry is two or
three fields, it's a repeating group.

## What the choice changes

- **Completion.** A single-entry item is complete when its one entry is submitted, or for
  PerApplicant, when every applicant it applies to has submitted theirs. A **multi-entry** Form
  item is complete only when the client has confirmed the list in Collect (the Continue on that
  section), it has at least `minInstances` entries, and every entry is submitted. So a multi-entry
  form that staff fill on the client's behalf doesn't move the deal on by itself until the client
  confirms it in Collect. Mention this to the user when the item is mostly staff-filled.
- **Optional items.** `isRequired` false means the step doesn't wait for the item.
  `minInstances` 0 means a multi-entry item can be confirmed with no entries. Pick the one that
  matches what the user means: "skip this if it doesn't apply" or "they may have none".
- **Rules.** A rule can refer directly to a form's answer only where there is exactly one answer to
  read:
  - From a Shared item, you can refer to Shared forms, and to PerApplicant forms with a single entry
    (it reads the answering applicant, else the primary).
  - From a PerApplicant item, you can refer to forms of the same applicant role, and to Shared forms
    with a single entry.
  - Anything with several entries, read across scopes, has no single answer. Use an aggregate
    condition instead (e.g. count of entries, any entry where..., sum of amounts). See
    `set_item_rules`.

  So decide scope and entries before writing rules. Changing them later can make an existing rule
  invalid.
- **Modules (Subject items).** The member forms of a module are normally Shared items, one entry
  each. See the `build-a-module` skill.

## Changing it later

- `update_item` changes `scope`, `minInstances`, `maxInstances` and `applicableRoles`. Setting scope
  Shared also clears `applicableRoles`.
- On a workflow that has never been published, live deals read these settings straight away, so a
  change alters what those deals need at once (see the `edit-a-published-workflow` skill). Check
  `list_workflows` for the status and confirm with the user first.
- Going from several entries to one, or from PerApplicant to Shared, can leave deals holding more
  answers than the item now expects. Confirm with the user before narrowing an item that's already
  in use.

## Quick reference

| The item is about... | scope | entries |
|---|---|---|
| the deal (purpose, amount, settlement date) | Shared | one |
| the security property | Shared | one, or several for multiple securities |
| each applicant (identity, residency, consent) | PerApplicant | one |
| each applicant's jobs, current and past | PerApplicant | several |
| each applicant's properties, loans, cards | PerApplicant | several, min 0 |
| a joint household budget | Shared | one |
| only guarantors | PerApplicant + applicableRoles | one |
| a short list inside one topic (dependants) | (that form's scope) | a repeating group in the form |
