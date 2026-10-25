# Connect ChatGPT

> **Status: coming soon.** ChatGPT identifies itself to ZiplineOS using a Client ID Metadata
> Document. ZiplineOS doesn't support this yet, so ChatGPT can't connect. This guide shows the
> intended setup.

*Last verified: 2026-10-14. ChatGPT's settings change often; look for the closest label.*

**Plans:** ChatGPT Plus, Pro, Business, Enterprise or Edu. On Business, Enterprise and Edu, a
workspace admin may need to allow developer mode or custom apps first.

## Set up

1. In ChatGPT, open **Settings → Apps & Connectors → Advanced** and turn on **Developer mode**.
2. Choose **Create** and enter:
   - Name: `ZiplineOS`
   - Description: `Build and edit ZiplineOS workflows and forms: find workflows, forms and questions by name; add and edit questions and show/hide rules; add stages and items; change a published workflow's next version (Release Candidate) for publishing in ZiplineOS.`
   - URL: `https://api.ziplineos.com.au/api/v1/mcp`
   - Authentication: **OAuth**
3. Choose **Create**, sign in to ZiplineOS, check the organisation on the consent screen, and
   approve.

## Use it

- In a chat, choose **+**, then developer mode / tools, and turn on **ZiplineOS**.
- For better results, paste [`microsoft/agent-instructions.md`](../microsoft/agent-instructions.md)
  into a Project's instructions, or into your custom instructions. Despite the folder name, it
  works with any assistant.
- ChatGPT asks before actions that change or remove data. Read each request before you approve
  it.

Once ZiplineOS is listed in ChatGPT's app directory, setup will be: **Apps → search
"ZiplineOS" → Connect**.

To disconnect, remove the app in ChatGPT, and revoke it in ZiplineOS under **personal settings → Security →
Connected AI apps**.
