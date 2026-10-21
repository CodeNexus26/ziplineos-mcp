---
name: build-a-calculation-engine
description: Build, test, validate and publish a ZiplineOS Logic calculation engine (Custom type) with the ZiplineOS MCP engine tools — inputs, computation steps (Formula, Table, Switch, Conditional), outputs and the optional response template. Use when a user asks to create, change, test or publish a calculator, calculation engine, serviceability or repayment calculation, stamp-duty table or similar in ZiplineOS Logic.
---

# Build a ZiplineOS calculation engine

A **calculation engine** (Logic portal) takes **parameters** (inputs), runs **computations** in
order, and returns **outputs**. Workflow integrations, Protocol nodes, quote estimates and the
engine's API/webhook can all run it.

The engine tools only work on **Custom** engines. Built-in engine types are refused. The
connector can delete an engine that was never published and isn't used anywhere (`delete_engine`,
ask first). It can't roll back a version, set up an engine's API/webhook access, or import one. A
person does those in ZiplineOS.

## Before you start

- **Access.** Every engine tool needs the Logic `engine_ai_authoring` permission, which is off by
  default, and the user's own access to calculation engines. *"Permission denied"* means it isn't
  switched on for them. Tell the user to ask their ZiplineOS administrator, and stop.
- **Never ask for ids.** `list_engines` lists the organisation's Custom engines (id, name,
  version, whether there are unpublished changes). Match by name; if several match, ask which.
- **Draft vs published.** Every edit changes the engine's **draft**. Once an engine has been
  published, everything that runs it uses the latest **published version** until you publish
  again. Two exceptions to tell the user about:
  - An engine that has **never been published** runs straight from its draft, so edits reach
    anything already using it at once.
  - A workflow integration can be **pinned** to one version (`pinnedVersion`). It keeps running
    that version after you publish.
  - Quoting collections that use the engine to enrich applicant data currently read its draft
    steps directly, so draft edits can show up in quotes before you publish.
- **A person may be editing too.** `get_engine` always reads the current draft. Call it before
  you change anything, and again after someone else may have edited. The last write to a step or
  output wins.

## 1. Plan with the user

Agree in plain language, before any write:

- the inputs (name, type, required or not, default);
- each calculation step, in order, and what it produces;
- which results are outputs, and their format (number, currency, percentage, text);
- a few test cases with the answers the user expects.

## 2. Build

1. `create_engine(name, description?)` makes a new empty Custom engine. To change an existing
   one, find it with `list_engines` and read it with `get_engine`.
2. `set_parameters(engineId, parameters)` **replaces the whole input list**, so send every
   parameter, including unchanged ones. Each has `key` (letters, digits and `_`, starting with a
   letter or `_`), `label`, `dataType` (`String`, `Number`, `Decimal`, `Boolean` or `Date`),
   `isRequired` and an optional `defaultValue`. Formulas refer to inputs by key.
3. `add_computation(engineId, key, label, type, configurationJson, position?)` adds a step. Steps
   run in order; omit `position` to append. `type` is `Formula`, `Table`, `Switch` or
   `Conditional`. The tool description has the exact configuration shape and an example for each
   type. Follow it exactly. Points that are easy to miss:
   - A formula can use inputs, results of **earlier** steps, and earlier expressions in the same
     step. It has `+ - * /`, brackets and the listed functions (`if`, `min`, `max`, `round`,
     `amortize`, …) only. There are no comparison operators: use `if(x, a, b)`, where a non-zero
     `x` means true.
   - Every value in table rows and switch cases is a JSON **string**. Switch case keys and
     table cells both match ignoring case. Switch keys that differ only by case are refused at
     publish.
   - Conditions use `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `contains`, not symbols like `>`.
   - A list can't contain `null` entries (expressions, table columns, rows or outputs,
     conditional branches); they are refused.
   - Unknown names in a formula quietly evaluate to 0. Saving a step only checks its basic shape,
     so a draft can save and still be wrong. `validate_engine` catches it.
4. `add_output(engineId, key, label, format?, position?, isVisible?)` exposes a result. `key` must
   be something a step produces (an expression's output, a table output key, a switch
   `outputKey`) or an input key.
5. Change things with `update_engine` (name, description), `update_computation` and
   `update_output`: only what you pass changes, but a new `configurationJson` **replaces the whole
   configuration**. Fix order with `reorder_computations` / `reorder_outputs`, passing **every**
   id exactly once. `delete_computation` / `delete_output` remove one and renumber the rest; ask
   first.
6. `set_output_schema` is optional and needs the user's explicit yes. When set, its JSON template
   (placeholders like `{{monthly}}`) **replaces the engine's response for every caller** and the
   outputs list is ignored. An empty value clears it.

## 3. Test

`test_engine(engineId, inputsJson)` runs the **current draft**, unpublished edits included, and
saves nothing. Live callers aren't affected. `inputsJson` is a JSON object keyed by input key,
for example `{"loan":500000,"years":30}`.

- Run the user's test cases and compare with the answers they expect. Show them the results.
- Keys ending in `_error`, also listed in `errors`, are evaluation problems. Fix them.
- Missing or misspelt input keys, and non-numeric values, quietly count as 0. A suspicious 0
  usually means a typo.
- To check an Integration item that uses the engine, use `test_integration(workflowTemplateId,
  itemId, answers)`. It runs the version the item really runs (its `pinnedVersion`, else the
  latest published) with its field mappings, on sample answers. No deal is involved and nothing is
  saved. A never-published engine is refused, so publish first (ask first).
- An Integration item's `resultsDisplay` with the `default` preset lists deal field names. On an
  engine item each must be one of the engine's visible outputs.

## 4. Validate

`validate_engine(engineId)` runs the same checks as publishing and returns an empty list when the
engine is ready. Issue codes: `NO_COMPUTATIONS`, `DUPLICATE_KEY`, `UNKNOWN_OUTPUT_KEY`,
`UNRESOLVED_VARIABLE` (a formula uses a name that isn't an input or an earlier result, including
a value set in only one branch of a conditional), `INVALID_CONFIG` and `UNRESOLVED_TEMPLATE_VAR`.
Fix each issue, re-test, and validate again until the list is empty.

## 5. Publish (ask first)

`publish_engine(engineId, changeNotes)` makes the draft the new live version. **Everything that
runs this engine (workflow integrations, Protocol nodes, quote estimates, API/webhook callers)
switches to it immediately**, except integrations pinned to an older version.

- Before publishing, tell the user what changed, the test results, and that live use switches
  straight away. Wait for an explicit yes.
- `changeNotes` is required. Write one plain sentence about what changed; it appears in the
  version history.
- A new engine's first publish is version 1.
- Renaming an engine or editing its description marks it as having unpublished changes. Publish
  to clear them.
- Publishing is refused while `validate_engine` reports any issue.
- `get_engine_versions` lists the published versions, newest first, with their notes. To go back
  to an earlier version, the user rolls back in ZiplineOS.

## Don't

- Don't publish without an explicit yes, and don't publish to "see if it works". Use
  `test_engine`.
- Don't tell the user a change is live until `publish_engine` has succeeded, unless the engine has
  never been published (then the draft is what runs).
- Don't guess formulas, rates or table values. Build only from what the user gives you, and ask
  when something is missing.
