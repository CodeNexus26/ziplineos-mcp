---
name: form-field-conventions
description: Rules for adding and editing ZiplineOS form fields through the ZiplineOS MCP tools — field keys, types, ordering, choice options, visibility rules, type-specific config (money/currency, number bounds, ABR lookup, disclaimers), nested forms and safe PATCH edits. Use whenever you call add_field, create_form_with_fields, update_field or delete_field, or when a user asks to add, change, move, hide/show or remove a question on a form.
---

# ZiplineOS form-field conventions

ZiplineOS forms are lists of fields (questions). A form is **Draft**, **Published** or
**Archived**, and may carry *unpublished changes*. Every rule below comes from how the tools
behave; when a tool's error message disagrees with this guide, believe the error.

## Find before you write

- Resolve forms by **name**: `list_forms(nameQuery)`. Never ask the user for an id. If more than
  one form plausibly matches, ask which one.
- To find a question inside a workflow, use `search_fields(workflowTemplateId, query)` or
  `list_workflow_fields(workflowTemplateId)`, not one `get_form` per form.
  - `search_fields` is a plain substring match on label or key. It misses related fields with
    different names (searching "address" will not find "suburb" or "postcode"). When the concept
    is broad, use `list_workflow_fields` and filter it yourself.
  - Rows for fields inside a nested (child) form carry `nestedUnderFieldKey` and the **child
    form's** `formTemplateId`. Edit those fields using that child `formTemplateId`.
- Before changing a field, `get_form` to see its current state, including its existing `rules`
  and config. You need this to confirm nothing you care about will change.

## Keys, labels, types

- `key` must match `^[a-z0-9_-]+$`: lowercase, digits, `_` or `-`, **no dots, no spaces**. Use
  `snake_case` that describes the data (`employer_name`, `gross_annual_income`). Keys are stable
  identifiers: don't rename a key on a form that already has submissions unless the user
  explicitly asks for it.
- Keys must be unique within a form. Check `get_form` first.
- `type` is one of: `Text`, `TextArea`, `Number`, `Money`, `Date`, `DateTime`, `Dropdown`,
  `Radio`, `MultiSelect`, `Checkbox`, `Email`, `Phone`, `Address`, `File`, `Files`,
  `ContactSelection`, `UserSelection`, `ApplicantSelector`, `Autocomplete`, `Lookup`,
  `EntityReference`, `Display`, `Image`, `BookingSlot`, `SubjectDelegation`, `NestedForm`,
  `Summary`.
  - Prefer the most specific type: `Money` for dollar amounts, `Email`/`Phone` for contact
    details, `Date` for dates, `Address` for addresses.
  - `Display` and `Image` hold no answer. A `Display` field's rich-text body goes in `helpText`.
  - `Summary` is a legacy type; don't create new ones.
  - The connector cannot create a working `NestedForm` field (see "Nested forms" below).

## Choice fields (Dropdown, Radio, MultiSelect)

- Supply `optionsJson` as `{"items":[{"value":"self_employed","label":"Self-employed"}]}`.
- `value` is what is stored and what visibility rules compare against; `label` is what the
  client sees. Use stable `snake_case` values.
- Before writing a rule that depends on an option, confirm the option exists. If the option the
  user mentions isn't there, say so and ask; don't invent it silently.

## Ordering

- `order` is **zero-based**. On `add_field` it inserts at that position and shifts later fields
  down; omit it to append at the end. On `update_field` it moves the field.
- Composite child fields (for example the hidden parts of an `Address`) always stay directly
  after their parent. Don't pass `order` for a child; move the parent instead.
- `create_form_with_fields` adds fields in **array order**. List them in the order the client
  should answer them.

## Visibility (show/hide) rules

- Prefer the structured `visibility` parameter to hand-written `rules` JSON:

  ```json
  {"action":"show","logic":"OR","conditions":[
    {"fieldKey":"employment_type","operator":"equals","value":"company"},
    {"fieldKey":"employment_type","operator":"equals","value":"trust"}]}
  ```

  - `action`: `show` or `hide`. `logic`: `AND` (default) or `OR`.
  - `operator`: `equals`, `notEquals`, `contains`, `notContains`, `greaterThan`, `lessThan`,
    `greaterOrEqual`, `lessOrEqual`, `isEmpty`, `isNotEmpty`.
  - `fieldKey` refers to a field **on the same form**. Use the option `value`, not its label.
- Relative-date conditions (`isEarlierThan`, `isLaterThan`, `isOnOrBefore`, `isOnOrAfter`) and
  rules that reference another form are **not** supported by `visibility`. They need raw `rules`
  JSON. If you're not sure of the exact shape, copy the shape from an existing field's `rules`
  (via `get_form`), or ask the user to set the rule in the ZiplineOS form builder.
- If you pass both `rules` and `visibility`, `rules` wins and `visibility` is ignored. Pass one.

## Editing an existing field: `update_field` is a PATCH

- Pass **only** the attributes you are changing. Everything you omit, including the field's
  visibility rule and type-specific config, stays exactly as it was.
- Do not "re-send" label, required, rules or options to be safe. Re-sending is how rules get
  overwritten by mistake.
- To clear something:
  - `helpText` / `placeholder`: pass `""`.
  - `rules`, `defaultValue`, `optionsJson`: pass the name in `clear`, e.g. `clear:["rules"]`.
  - A new `rules`/`visibility` in the same call wins over `clear:["rules"]`.
- `configJson` on `update_field` overlays only the keys you include; other config keys are left
  alone.
- Changing `type` keeps the other attributes. Make sure the result makes sense (e.g. options on
  a field that is no longer a choice field).
- After an edit, re-read with `get_form` (or `search_fields`) and confirm the change, and that
  any existing rule is still there.

## Type-specific settings (`configJson`)

`configJson` is a JSON object of extra field settings. Unknown keys are **rejected** (the error
names the key), and attributes that have their own parameter (label, required, options, rules,
default value, help text, placeholder, internal-only…) must use that parameter. Common keys:

| Need | Field type | `configJson` |
|---|---|---|
| Australian Business Register lookup | `Lookup` | `{"externalLookupProvider":"Abr"}` |
| Number bounds (integers) | `Number`, `Money` | `{"minValue":0,"maxValue":5000000}` |
| Allow a non-AUD currency | `Money` | `{"allowCurrency":true,"defaultCurrency":"NZD"}` |
| Prefix/suffix text | input fields | `{"prefix":"$","suffix":"p.a."}` |
| Disclaimer with a consent tick | `Checkbox` | `{"displayHint":"disclaimer","disclaimerBody":"<p>…</p>","disclaimerCheckboxLabel":"I agree","disclaimerRequireScroll":true}` |
| Repeatable nested form | existing `NestedForm` | `{"isRepeatable":true,"minRepetitions":1,"maxRepetitions":0}` (0 = unlimited) |
| Search a list of values | `Autocomplete` | `{"lookupListId":"<id>"}` |
| Pick another submission on the deal | `EntityReference` | `{"referenceTargetKind":"FormSubmission","referencedFormTemplateId":"<form id>","referenceScope":"Deal"}` |

Notes:

- **Currency.** `Money` amounts are AUD unless `allowCurrency` is true. `defaultCurrency` is an
  ISO 4217 code and only matters when `allowCurrency` is true. Leave currency alone for normal
  Australian amounts.
- `minValue`/`maxValue` must be whole numbers.
- There is no tool to list lookup lists, so you can't discover `lookupListId` values. Ask the user,
  or have them configure the field in ZiplineOS.
- `bindsTo` (writing an answer through to the contact record, e.g. `Contact.Email`) changes
  CRM data when the form is submitted. Only set it when the user asks for it.
- `get_form` returns every config attribute, so read it, then patch only the key you need.

## Other field flags

- `required`: the client must answer before submitting. Only set it if the user asked, or the
  question is clearly mandatory.
- `isInternalOnly`: broker-only; the field is not shown to the client. `add_field` has no
  parameter for it, so add the field, then set it with `update_field`.
- `requireLater` (`File`/`Files`): the document is collected later through the Documents
  section instead of inline. It never blocks the form from completing.

## Nested forms

- A `NestedForm` field embeds a child form (e.g. one asset or liability). The connector can
  **read** nested forms (`get_form` shows `nestedFormTemplateId`; `list_workflow_fields` walks
  into them) and **edit the child form's fields** directly, but it **cannot link** a child form
  to a `NestedForm` field. If the user needs a new nested form, build the child form with the
  tools, then ask them to attach it in the ZiplineOS form builder.
- Publishing a parent form also publishes its nested forms, and fails if one of them is
  archived.

## Removing and undoing

- `delete_field` removes a field (soft delete) and marks the form as having unpublished changes.
  Confirm with the user before deleting a field that may already hold client answers.
- `discard_form_changes` reverts **all** unpublished edits on a form back to its last published
  version. It does nothing on a form that has never been published. It's the undo for a bad
  edit, but it also throws away any other unpublished edits on that form, so check first.

## Publishing a form

- Field edits stay unpublished until `publish_form`. **Publishing makes the changes visible to
  test and preview deals at once**, and to live deals once each workflow using the form is
  published in ZiplineOS. Always ask the user before publishing a form that is already in use. Say which
  form, summarise the changes, and wait for a clear yes.
- A new form must be published once before it can be linked to a workflow item.
- Never publish as a side effect of an edit the user didn't ask to go live.
