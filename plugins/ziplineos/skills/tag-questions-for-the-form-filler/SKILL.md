---
name: tag-questions-for-the-form-filler
description: How to tag a ZiplineOS workflow's questions with data points so the ZiplineOS Chrome extension form filler can fill another website (for example Platform Plus) from a deal's answers, using get_profile_coverage, list_question_tags, list_data_points, set_question_tags and delete_question_tag. Use when a user asks to rig up, map or tag a workflow or fact find for the form filler, Platform Plus or another website, or asks why a question isn't being filled.
---

# Tag questions for the form filler

The Chrome extension fills other websites (for example Platform Plus) from a deal's answers. It
doesn't read question labels. It reads **data points**: shared names such as
"applicant.identity.first_name". Each website has a fill profile that says which data point goes into
which field on that site. A question's answer reaches the site only when the question is **tagged**
with the data point the profile expects.

A tag belongs to the question, not the website. One tag serves every website whose profile uses that
data point.

## Rig up a workflow

1. Resolve the workflow with list_workflows.
2. Run get_profile_coverage with the workflow and the website ("platformplus" covers both Platform
   Plus profiles: the client portal fact find and AMS). Its "profiles" say which fill each website is
   reported on (see "Two fills" below); every row's "fillPath" says the same.
3. For each "missing" or "matched_by_field_key" data point, pick the question that holds that answer. The "suggestions" are a
   starting point matched on wording; they can be wrong. When none fits, or more than one could, ask
   the user which question it is. Never tag a question just because it is the only suggestion.
4. Tag them in one set_question_tags call (up to 100 tags). Read every result and fix the refused ones:
   the usual cause is a question type that can't feed the data point (list_data_points lists the types
   that can).
5. Run get_profile_coverage again and report what is still "missing".

## Two fills

The extension fills a website one of two ways, and they read different data points:

- **fill_plan**, the newer fill. Only tagged questions fill. It reads its own set of data points: for
  example the Platform Plus portal takes the whole address from "applicant.address.full" (tag the
  Address question with it) and splits it itself. A website is reported on its fill plan when it has
  one and you have the form filler fill plan permission. "active": false means the org hasn't tagged
  any of its data points yet: the older fill runs until the first such tag, then the fill plan takes
  over for the whole org. So tag for the fill plan's data points, not the older fill's.
- **legacy**, the older fill. It also fills a question whose key is the same as the data point
  ("matched_by_field_key").

The extension decides per user, by the permission of whoever set it up. A teammate without the fill
plan permission still gets the older fill.

## Things to know

- "matched_by_field_key" works only on the older fill. Once the org's tags move a website onto the
  fill plan, only tagged questions fill. So tag these too: the suggestion is the question with that key.
- A question hidden in the form builder, or any question inside a hidden NestedForm question, is never
  filled. list_question_tags marks it "isHiddenQuestion"; don't tag it, and get_profile_coverage
  leaves it out.
- The generated parts of a visible question (for example an Address question's suburb and postcode)
  can be tagged for the older fill, which sends them. The fill plan never sends them: it uses the
  visible question itself (tag the Address question with "applicant.address.full").
- "not_in_dictionary" keys aren't data points yet, so they can't be tagged. Only a question with that
  exact key feeds them. Tell the user; don't rename keys to force a match unless they ask.
- Questions inside a NestedForm (for example one row per asset) are tagged on the nested form: use the
  "formTemplateId" that list_question_tags returns for that row.
- Repeating data points (one per applicant, one per employer) are filled per instance by the filler.
  Tag the question once; don't create one question per applicant.
- A tag replaces the question's previous tag. delete_question_tag removes one.
- Tags apply to the form filler straight away, on every deal that uses the form. They don't change
  what clients see.
