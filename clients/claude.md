# Connect Claude (web, desktop, mobile)

*Last verified: 2026-10-14. Claude's menus change from time to time; if a label differs, look
for the closest match.*

You need a paid Claude plan that supports custom connectors, a ZiplineOS account, and the
connector switched on for your ZiplineOS organisation.

## Individual plans (Pro, Max)

1. In Claude, open **Customize → Connectors**, choose **+ Add**, then **Add custom connector**.
2. Name: `ZiplineOS`. URL: `https://api.ziplineos.com.au/api/v1/mcp`
3. Under the OAuth client options, choose **Use your own OAuth client** and enter
   Client ID `zipline-mcp`. Leave the client secret blank. Don't choose "Use Claude's published
   identity" or "Register automatically" — ZiplineOS doesn't support them yet.
   <!-- Once ZiplineOS supports
   Client ID Metadata Documents, switch this step to "Use Claude's published identity". -->
4. Choose **Add**, then **Connect**.
5. Sign in to ZiplineOS if asked, check the organisation shown on the consent screen, and choose
   **Approve**.

Connectors you add on the web also appear in Claude Desktop and the mobile apps.

## Team and Enterprise

An organisation **Owner** adds the connector once:

1. **Organization settings → Connectors → Add → Custom** (choose **Web** if asked).
2. Enter the same name, URL and OAuth client ID as above, then **Add**.

Each member then opens **Customize → Connectors**, finds ZiplineOS, and chooses **Connect**.
Everyone signs in with their own ZiplineOS account, so their own permissions apply.

## Add the skills (recommended)

The skills teach Claude the safe way to build and edit workflows.

1. Download this repository and zip each folder under
   [`plugins/ziplineos/skills/`](../plugins/ziplineos/skills/) separately (for example
   `build-a-workflow.zip` containing the `build-a-workflow` folder).
2. In Claude, open **Customize → Skills**, choose **+ → Create skill → Upload a skill**, and
   upload each zip. Code execution must be enabled for skills to work.

Team and Enterprise Owners can provide skills to the whole organisation instead.

## Use it

- In a chat, open the tools menu and make sure **ZiplineOS** is on.
- Try: *"List my workflows and summarise the steps in the fact find."* More in
  [`prompts/`](../prompts/).
- Claude asks before actions that change or remove things. Read the request before you approve
  it.

## If something's wrong

- **Tools missing or out of date** after a ZiplineOS update: remove the connector and add it
  again. Refreshing the page isn't enough, because Claude keeps the old tool list.
- **Asked to sign in again**: sessions expire after a few hours. Choose **Connect** again.
- More in [docs/troubleshooting.md](../docs/troubleshooting.md).

To disconnect, remove the connector in Claude, and disconnect it in ZiplineOS under **personal
settings → Security → Connected AI apps**. Access ends straight away.
