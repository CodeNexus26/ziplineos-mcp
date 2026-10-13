---
name: fact-find-patterns
description: Common shapes for Australian mortgage-broking fact finds and loan application workflows in ZiplineOS — typical sections, question types and conditional questions (PAYG vs self-employed, ABR lookup, joint applicants, money fields). Use when a user asks to design, build, extend or review a fact find, loan application, client intake or serviceability questionnaire, or asks what questions a home-loan form should have.
---

# Fact-find patterns (Australian mortgage broking)

These are **starting points**, not requirements. Every brokerage, aggregator and licensee has
its own fact find. Follow the user's and their licensee's requirements over these suggestions.
Don't tell a user their fact find is "compliant": that's a judgement for them and their
compliance team.

## Reuse before you build

Many organisations already have a fact find in ZiplineOS. Before designing one:

1. `list_workflows(nameQuery:"fact find")` and `list_forms(nameQuery:"…")` for "applicant",
   "employment", "income", "expenses", "assets", "liabilities".
2. `list_workflow_fields` on an existing fact-find workflow shows every question at once,
   including nested forms.
3. Offer to extend what exists (see `edit-a-published-workflow`) before creating a parallel
   version.

## Typical sections

One form per section keeps forms short and lets a section be reused across workflows.

| Section | Typical questions (type) |
|---|---|
| Applicant details | title (`Dropdown`), first/middle/last name (`Text`), date of birth (`Date`), email (`Email`), mobile (`Phone`), current address (`Address`), time at address, marital status (`Dropdown`), residency status (`Dropdown`: citizen / permanent resident / visa holder) |
| Household | number of dependants (`Number`), dependants' ages |
| Employment | employment type (`Radio`: PAYG full-time / part-time / casual / self-employed / contractor / not employed), employer (`Text`), occupation, start date (`Date`) |
| Self-employed | business name (`Lookup` with `{"externalLookupProvider":"Abr"}`), years trading, entity type (sole trader / company / trust / partnership) |
| Income | base salary, overtime, bonus, rental income, other income (`Money` each) |
| Living expenses | categories as separate `Money` fields with a frequency (`Dropdown`: weekly / fortnightly / monthly / annually) |
| Assets | property, savings, superannuation, vehicles (`Money` values plus descriptions) |
| Liabilities | home loans, credit cards (limit and balance), personal and car loans, HECS/HELP (`Money`) |
| Loan requirements | purpose (`Dropdown`: purchase / refinance / construction / investment), loan amount (`Money`), term (`Number`), repayment type (`Radio`: principal & interest / interest only), rate preference (`Radio`: variable / fixed / split), offset or redraw needed (`Checkbox`) |
| Objectives | the client's goals and priorities in their own words (`TextArea`) |
| Consent | privacy / credit-check consent: a `Checkbox` in disclaimer mode with the licensee's own wording (see `form-field-conventions`) |
| Documents | ID, payslips, bank statements, tax returns: `File`/`Files` fields, with `requireLater` when they're collected after the form |

## Conditional questions that come up a lot

- **Self-employed only**: show the business questions when `employment_type` equals
  `self_employed` (structured `visibility`, `action:"show"`). For several matching values (company
  *or* trust), use `logic:"OR"` with one condition per value.
- **Previous address**: show previous-address questions when time at current address is under
  the user's threshold. If time at address is a `Number` of years, use `lessThan`.
- **Visa details**: show visa type and expiry when residency status equals `visa_holder`.
- **Interest-only period**: show when repayment type equals `interest_only`.

Use option **values** in conditions (`self_employed`), never the display label.

## Money and numbers

- Use `Money` for every dollar amount (AUD by default; leave currency settings alone unless the
  user deals in foreign income or assets).
- Pair amounts with a frequency field rather than assuming annual.
- Add sensible bounds only when the user asks (`configJson` `minValue`/`maxValue`, whole numbers).

## Joint applicants, assets and liabilities

Lists of things (each asset, each liability, each co-applicant's employment) are usually
**repeatable nested forms** in ZiplineOS. The connector can build and edit the child form, but
can't attach it to a `NestedForm` field. Build the child form, then ask the user to attach it in
the ZiplineOS form builder. Or reuse an existing nested form that is already set up.

## Workflow shape

A common shape: **Lead / enquiry → Fact find → Document collection → Assessment → Lodged →
Conditional approval → Unconditional approval → Settled (Won)**, plus **Not proceeding (Lost)**.
Confirm the user's own stage names. Don't impose this list.
