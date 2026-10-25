---
name: edit-a-published-workflow
description: Safe procedure for changing a ZiplineOS workflow that is already Published using the ZiplineOS MCP tools — edit its Release Candidate directly, review with the human, and hand over for publishing in ZiplineOS. Also covers editing forms that deals already use, and undo/discard. Use when a user asks to change, fix, rename, reorder or remove anything in an existing published workflow or a form that is in use, or when a tool says a workflow "has a draft loaded in its editor".
---

# Edit a published workflow safely

The connector edits a workflow's **Release Candidate** (RC): the next version, waiting to go
live. Every structure tool (`add_step`, `update_step`, `add_item`, `update_item`, `move_item`,
`reorder_*`, `set_item_rules`, `set_step_rules`, `delete_*`, `update_workflow`) changes the RC and
nothing else. The RC reaches only **test and preview deals**. Live deals keep running the version
that was last published, until a person **publishes the workflow in ZiplineOS**. The connector
can't publish a workflow.

Drafts and merging are done in ZiplineOS, not through the connector. Forms work differently:
they're versioned on their own (see "Editing forms that are in use").

## Words to use with the user

- **Release Candidate (RC)**: the next version of the workflow. Test and preview deals run it;
  live deals don't, until it's published in ZiplineOS.
- **Published version**: what live deals run now.

## Procedure

1. **Find it.** `list_workflows(nameQuery)`, then `get_workflow` to see its status and structure.
   If more than one workflow matches, ask which.
2. **Check what the editor has open.** `get_workflow` returns `editingDraftId`. `null` means the
   editor has the Release Candidate open and you can edit it. If it's set, a person has loaded a
   draft in the ZiplineOS editor; you can read the workflow but not change it (see below).
3. **Edit.** Use the normal structure tools. `update_step` and `update_item` change only what you
   pass. Tell the user that test and preview deals see the change straight away, including any
   trigger or delay you set: test and preview deals **do** run triggers.
4. **Review with the user.** `get_workflow`, then summarise the differences from what was there.
5. **Hand over.** Tell the user the changes are in the Release Candidate. They reach live deals
   only once someone **publishes the workflow in ZiplineOS**.

## When a tool says the workflow "has a draft loaded in its editor"

The refusal reads *"Workflow '…' has a draft loaded in its editor. This connector edits only the
Release Candidate — switch the editor back to the Release Candidate in ZiplineOS before editing
here."* Someone has a draft open in the ZiplineOS workflow editor. The connector never edits a
draft.

1. **Stop. Don't retry and don't work around it.**
2. **Tell the user**: to edit here, they (or whoever has the draft open) switch the workflow
   editor back to the Release Candidate in ZiplineOS. A colleague may be in the middle of that
   draft, so they should check first.
3. Once `get_workflow` shows `editingDraftId: null`, carry on from step 3 of the procedure.

An **Archived** workflow is refused too: *"Workflow '…' is Archived. Unarchive it in ZiplineOS
before editing."* Unarchiving is done in ZiplineOS.

## Editing forms that are in use

Forms aren't part of the workflow's Release Candidate. `add_field`, `update_field` and
`delete_field` work on a form directly and leave it with **unpublished changes**. Deals keep
seeing the last published version of the form until `publish_form`.

- Make the edits, re-read with `get_form`, summarise them, then **ask before `publish_form`**.
  Publishing makes the form's changes visible to test and preview deals at once, and marks every
  workflow that uses it as having unpublished changes. Live deals see them only after that
  workflow is published in ZiplineOS. Say so plainly.
- To undo, `discard_form_changes` reverts all unpublished edits on that form (including anyone
  else's). Check `hasUnpublishedChanges` in `list_forms`, and ask before discarding edits you
  didn't make.

## Things that need an explicit yes every time

These change or remove existing work. Name the object, say what will happen, and wait for
confirmation:

- `publish_form` on a form that is in use.
- `archive_form`: removes the form from every workflow item that links it. Existing deal
  snapshots are kept. `unarchive_form` brings the form back as a Draft, but doesn't restore the
  links.
- `delete_step` (also deletes its items), `delete_item`, `delete_field`.
- `discard_form_changes`.
- Setting a trigger or delay on an Action or Integration item: it runs on every test and preview
  deal that qualifies, and Integrations may make paid calls.

## Don't

- Don't try to work around *"has a draft loaded in its editor"*. Ask the user to switch the editor
  back to the Release Candidate in ZiplineOS.
- Don't tell the user a workflow change is live. It reaches live deals only after the workflow is
  published in ZiplineOS.
- Don't tell the user a form change is live after `publish_form` alone, or after editing a form
  without publishing it.
- Don't batch unrelated changes without telling the user. Everything you change lands in the same
  Release Candidate and goes live together.
