# Troubleshooting

## "The workflow-authoring MCP connector is not enabled"

The connector isn't switched on for your environment or organisation. Ask your ZiplineOS
administrator.

## Sign-in loops, or you're asked to sign in again

- Make sure you're signed in to ZiplineOS in the same browser, then try **Connect** again.
- Sessions currently expire after a few hours, so reconnecting is expected for now. Longer-lived
  sign-in is coming.
- On the consent screen, check that the organisation is the one you expect. If you belong to
  several organisations, switch to the right one in ZiplineOS first.

## A tool is "missing", or behaves as if it has old options

AI clients cache the tool list from when you connected. After a ZiplineOS update:

- **Claude (web/desktop):** remove the connector and add it again. Refreshing the page or starting
  a new chat isn't enough.
- **Claude Code:** `/mcp` → reconnect, or restart Claude Code.
- **Copilot Studio:** refresh the MCP tool in the agent's **Tools**.

## "Workflow '…' has a draft loaded in its editor"

Working as intended. The assistant edits only a workflow's Release Candidate, never a draft.
Someone has a draft open in the ZiplineOS workflow editor. Switch the editor back to the Release
Candidate in ZiplineOS (check nobody is mid-way through that draft), then ask again.

## "Workflow '…' is Archived"

Unarchive the workflow in ZiplineOS before asking the assistant to edit it.

## "Item was not created … any linked form is published"

Form items can only link a **published** form. Publish the form first, then add the item.

## "configJson key '…' is not recognized"

That setting can't be set through `configJson`. It's either not supported, or it has its own
parameter (for example `required` or `helpText`). The error names the key.

## A change isn't showing on live deals

- Form edits stay unpublished until the form is **published**. A published form change reaches
  test and preview deals at once, and live deals once the workflow is published in ZiplineOS.
- Workflow changes land in the Release Candidate, which only test and preview deals run. They go
  live only when someone **publishes the workflow in ZiplineOS**. The assistant can't do this.
- Calculation engine changes go live only when someone publishes the engine in the ZiplineOS
  Logic portal. The assistant can't do this either.

## The assistant can't see a workflow, stage or form

It sees exactly what your ZiplineOS account can see. Some stages (for example Lead stages) and
features need extra permissions. Ask your ZiplineOS administrator.
