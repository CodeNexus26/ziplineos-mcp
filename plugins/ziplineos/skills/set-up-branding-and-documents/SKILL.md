---
name: set-up-branding-and-documents
description: Set a ZiplineOS organisation's brand colour, logo and alternate logo, check logo contrast, and change AI document settings (rename and extraction confidence, document categories and naming formats) with the ZiplineOS MCP org settings tools. Use when a user asks to set or change their brand colour or logo, fix a logo that is hard to see, or tune how documents are auto-renamed, auto-filled or categorised.
---

# Set up branding and AI document settings

These seven tools change settings for the user's **own organisation** (the one they are signed in
to): `get_branding`, `update_branding`, `get_document_ai_settings`, `update_document_ai_settings`,
`add_document_category`, `update_document_category` and `delete_document_category`. Changes to
branding and AI document settings are recorded in the audit log.

## Before you start

- **Role.** Every one of these tools needs the **Owner or Admin** role in the user's own
  organisation. There is no platform-admin bypass. If a tool is refused, tell the user to ask an
  Owner or Admin of their organisation, and stop.
- **Document tools need one more permission.** The AI document tools also need the AI Document
  Settings (`drive_ai`) permission: View to read, Manage to change.
- **Read first.** Call `get_branding` or `get_document_ai_settings` before you change anything,
  so you can tell the user what it is now and what will change.

## Branding

`get_branding` returns the brand colour, the logo URL and the alternate logo URL, plus `advice`.

1. Read the current state with `get_branding`.
2. Call `update_branding(brandColor?, logoUrl?, logoAltUrl?, clear?)`. It is a PATCH: only the
   fields you pass change.
   - The colour is `#RRGGBB`.
   - Logos are set by **https URL only**. You can't upload a file. The image must be PNG, JPEG or
     WebP, with a transparent background, under 2 MB. The server fetches each changed URL to
     detect whether the logo is light or dark.
   - To remove a value, list it in `clear` (`brandColor`, `logoUrl`, `logoAltUrl`). A blank value
     is refused, and so is giving and clearing the same field.
   - If the stored colour isn't `#RRGGBB` (it was saved elsewhere), a change that doesn't set
     `brandColor` is refused with guidance. Set a valid colour in the same call.
3. Read the returned `advice` and tell the user in plain language. It covers:
   - each logo's detected tone (light, dark or unknown), and which logo shows on light and on dark
     backgrounds;
   - whether a logo sits on a plate, and the plate colour;
   - whether an alternate logo is needed (`alternateNeededFor`) and what tone it should be
     (`alternateShouldBe`), or that a same-tone alternate is being ignored;
   - the brand colour's contrast with white, and any `warnings` (for example low contrast);
   - if a tone couldn't be checked, why.

## AI document settings

`get_document_ai_settings` returns two thresholds and the document categories.

- **Thresholds.** `update_document_ai_settings(renameConfidence?, extractionConfidence?)` is a
  PATCH, values 0.5 to 1.0. `renameConfidence` is the minimum confidence before a file is
  auto-renamed. `extractionConfidence` is the minimum before a form field is auto-filled from a
  document. A higher value means fewer but safer automatic changes.
- **Categories.** Each has a name, an optional naming format and `isDefault`.
  - `add_document_category(name, namingFormat?)`, `update_document_category(name, newName?,
    namingFormat?, clearNamingFormat?)` and `delete_document_category(name)` find a category by
    name, ignoring case.
  - Names are unique ignoring case and at most 100 characters. If two categories share a name, the
    call is refused: ask the user to rename one in ZiplineOS.
  - The naming format is optional free text that the AI reads as an instruction, for example
    "Surname - document type - issue date". At most 500 characters. A blank format is refused: use
    `clearNamingFormat` to remove it.
  - Renaming a built-in default makes it a custom category.
  - The last category can't be deleted. An empty list brings the defaults back.
- **When it applies.** Threshold and category changes apply to **newly processed documents**.
  Existing file names don't change.

## Confirm first

Wait for an explicit yes before you:

- change the brand colour or a logo (every user and client sees it straight away);
- change either confidence threshold;
- delete a category, rename a category, or change a naming format.

Say what it is now, what it will become and when it takes effect.

## Don't

- Don't ask for a file upload or paste image data. Ask for an https URL to the logo.
- Don't guess a colour or a naming format. Use what the user gives you, and ask when it is missing.
- Don't tell the user branding looks fine until you have read `advice` and passed on its warnings.
