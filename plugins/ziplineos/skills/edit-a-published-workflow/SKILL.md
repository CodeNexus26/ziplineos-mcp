---
name: edit-a-published-workflow
description: Safe procedure for changing a ZiplineOS workflow that is already Published (live) using the ZiplineOS MCP tools — open a draft, load it, edit, merge into the Release Candidate, resolve conflicts with the human, finalise. Also covers editing forms that live deals already use, and undo/discard. Use when a user asks to change, fix, rename, reorder or remove anything in an existing live workflow or a form that is in use, or when a tool says a workflow is Published with no draft loaded.
---

# Edit a published workflow safely

Live deals run on published workflows, so the connector never edits a published workflow's
structure directly. Steps and items change on a **draft**. The draft is merged into the
workflow's **Release Candidate** (RC): the next version, waiting to go live. **Going live is done
by a person in ZiplineOS.** The connector stops at the RC.

Forms work differently: they're versioned on their own (see "Editing forms that are in use").

## Words to use with the user

- **Release Candidate (RC)**: the next version of the workflow, not yet live.
- **Draft**: a private working copy taken from the latest published version.
- In conflicts, **KeepCurrent** = keep the **Release Candidate's** version; **KeepOther** = keep
  the **draft's** version. Always explain choices in these plain terms.

## Procedure

1. **Find it.** `list_workflows(nameQuery)`, then `get_workflow` to see its status and structure.
   If more than one workflow matches, ask which.
2. **Open a draft.** `list_drafts` first: if the user already has a suitable draft, reuse it.
   Otherwise `create_draft(workflowTemplateId, name)` with a descriptive name (e.g.
   "Add trust step – Oct"). If a draft shows `baseIsStale: true`, the live workflow has moved on
   since that draft was taken; expect conflicts at merge, or start a fresh draft.
3. **Load the draft.** `switch_editor_context(workflowTemplateId, target:"Draft", draftId)`.
   This changes which version the workflow editor has open, for this workflow, in ZiplineOS.
   Tell the user before you do it, in case a colleague is editing the same workflow.
   If the workflow has live deals and the draft already changes how they run, loading it is
   refused (see "When an edit is refused because of live deals" below).
4. **Edit.** Use the normal structure tools (`add_step`, `update_step`, `add_item`,
   `update_item`, `move_item`, `reorder_*`, `delete_*`). With the draft loaded, edits land on the
   draft, not the live workflow. `update_step` and `update_item` change only what you pass.
   On a workflow with live deals, some of these edits are refused; see the next section.
5. **Review with the user.** `get_workflow`, then summarise the differences from what was there.
6. **Merge.** `merge_draft_into_rc(draftId)`.
   - `conflictsRequireResolution: false`: done. The RC now holds the changes.
   - `conflictsRequireResolution: true` with a `sessionId`: go to step 7.
7. **Resolve conflicts with the human.**
   1. `get_merge_conflicts(sessionId)`. Each conflict has a label, a change kind, and a headline
      for each side (`currentSideLabel` = the RC, `otherSideLabel` = the draft).
   2. For **each** conflict, propose `KeepCurrent` or `KeepOther` with a one-line reason, in a
      list the user can read.
   3. **Wait for the user to confirm.** Don't choose on their behalf, even if it looks obvious.
   4. `apply_conflict_resolutions(sessionId, resolutions)`. Each `choice` must be exactly
      `KeepCurrent` or `KeepOther`; no other value is accepted.
   5. `finalize_merge(draftId, mergeSessionId)`. If it says conflicts are unresolved, fetch them
      again and repeat.
8. **Hand over.** Tell the user the changes are in the Release Candidate and must be **published
   in ZiplineOS** to reach live deals. Ask whether to switch the editor back to the RC
   (`switch_editor_context(target:"Rc")`).

## When an edit is refused because of live deals

While a draft is loaded, the published workflow's steps and items **are** the draft: ZiplineOS
writes the draft into the same tables live deals run from. So on a published workflow that has
live deals (test deals don't count), ZiplineOS refuses any edit that would change what those deals
run **straight away**, even though the draft isn't published. The refusal starts *"Can't … while a
draft is loaded: this workflow is published and has live deals"* (in ZiplineOS's own API it is a
409 with code `workflow_draft_live_guard`). The same rule applies in the ZiplineOS editor, not
just the connector.

Refused while a draft is loaded and live deals exist:

- An item's trigger or delay, its Action/Integration config (even on a manual item, because a
  person can still run it), or its reactions. Also the rules of an item that runs on its own (it
  has an automatic trigger or a delay).
- Adding an item that runs on its own, has reactions, or is an Action/Integration with config.
- Moving an item that runs on its own to another step.
- Step rules: changing enabled rules, or turning them on or off. Adding a step with rules on.
- On steps live deals can be on: renaming, deleting, changing `isTerminal` or `stageType`,
  changing their order relative to each other, and flipping `isRequired` on an existing item.
- Loading (`switch_editor_context`) a draft that **already** contains any of those changes, for
  example one written while the workflow had no live deals, or one updated by a merge.
- In ZiplineOS, setting the workflow back to Draft while it has live deals.

When this happens:

1. **Stop. Don't retry and don't work around it.** Don't try another tool, a raw-JSON parameter,
   a different draft or an unpublished-then-republished workflow to get the same change in.
2. **Explain it plainly**, for example: "ZiplineOS won't let me change that while this workflow
   has live deals. The draft is stored in the same place those deals run from, so the change would
   reach them straight away, before anyone has published it."
3. **Say what still works**, and let the user choose:
   - Edits that don't change what runs: adding Form, Checklist or document items, renaming
     items, deleting items, repositioning an item within its step, adding a step without rules, and
     renaming, re-staging, reordering or deleting a step that exists only in this draft and has
     no live deals on it. Show/hide rules on items that don't run on their own, and step rules
     that stay switched off, are also fine.
   - Switching an item's trigger to manual (a disarm) is always allowed. Runs already scheduled
     on deals still go ahead.
   - Question and form changes: forms are versioned on their own. Edit the form and use
     `publish_form` after the user agrees (see below).
   - A draft that already holds the change can still go live without being loaded:
     `merge_draft_into_rc(draftId)` merges it into the Release Candidate, and a person publishes
     the RC in ZiplineOS. If `switch_editor_context` refused to load a draft, offer this. If
     another draft is loaded now, switching to the RC first can also make a different draft
     loadable, because the check compares against what is loaded.
   - Otherwise the change has to wait until no live deals run on the workflow, or the user makes
     it in a copy of the workflow that isn't live yet.

## Editing forms that are in use

Forms aren't edited through workflow drafts. `add_field`, `update_field` and `delete_field` work
on a form directly and leave it with **unpublished changes**. Live deals keep seeing the last
published version until `publish_form`.

- Make the edits, re-read with `get_form`, summarise them, then **ask before `publish_form`**.
  Publishing changes what every live deal using that form sees. Say so plainly.
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
- `delete_step` (also deletes its items), `delete_item`, `delete_field`, `delete_draft`.
- `discard_form_changes`, `discard_release_candidate` (throws away all unpublished changes in the
  RC).
- `apply_conflict_resolutions`, `finalize_merge`.

## Don't

- Don't try to work around *"Published with no draft loaded"*. That error is the safety rail;
  follow the procedure above.
- Don't retry or route around a *"while a draft is loaded … has live deals"* refusal. It protects
  live deals from unpublished changes.
- Don't tell the user a change is live after `finalize_merge` or after editing a form without
  publishing. It isn't.
- Don't batch unrelated changes into one draft without telling the user. One draft per change
  set makes conflicts easier to read.
