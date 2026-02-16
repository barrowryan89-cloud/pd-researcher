# Link Health Log — Distribution Sprint

**Last run:** Feb 15, 2026 @ 08:28 UTC  
**Operator:** PD (Autonomous Promotion Engine)

| Asset | Command | Result | Notes |
|-------|---------|--------|-------|
| GitHub Repo | `curl -I https://github.com/barrowryan89-cloud/pd-researcher` | **404** | Repo still private when logged out. Either flip it public before Show HN or mention the invite status inside the launch copy so moderators aren’t surprised. |
| Vercel Landing | `curl -I https://workspace-ivory-one.vercel.app` | **200 OK** | Fresh redeploy with expanded `vercel.json` now serves every static asset. |
| Direct ZIP | `curl -I https://workspace-ivory-one.vercel.app/pd-researcher.zip` | **200 OK** | 238 KB ZIP downloadable straight from Vercel; include in first-comment macros. |
| HTML Converter Demo | `curl -I https://workspace-ivory-one.vercel.app/html-converter.html` | **200 OK** | Demo link works again; screenshot it for Show HN replies. |
| Text Summarizer Demo | `curl -I https://workspace-ivory-one.vercel.app/text-summarizer.html` | **200 OK** | Live proof for “does it work?” questions. |
| Raw Tool Endpoint | `curl -I https://workspace-ivory-one.vercel.app/tools/json_formatter_free.py` | **200 OK** | Individual CLI files can now be `curl`’d directly from the mirror; use this in community-answer macros. |

## How to Re-Run
1. Make sure `vercel.json` still includes the glob patterns for `*.html`, `*.zip`, `public/**/*`, and `tools/**/*.py`.
2. From the repo root run `vercel deploy --prod --yes` to push the latest static bundle.
3. Re-run each `curl -I` command above (or use `xargs -n1 curl -I`) and update the table + timestamps.
4. Paste the new summary into README’s “Link Health Monitor” block and drop the receipts inside `content/distribution_receipts.md`.

Keeping this sheet current means moderators immediately see that mirrors are alive—even if GitHub is still private.
