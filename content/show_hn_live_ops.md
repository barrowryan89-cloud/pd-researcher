# Show HN Live Ops Playbook — Feb 17, 2026

**Objective:** Launch "Show HN: 59 Free CLI Tools (Zero Dependencies)" during the 8–10 AM PST peak slot, convert traffic to stars, email captures, and directory momentum. No code changes — pure distribution.

## 🔁 Timeline (UTC)
| Time (UTC) | Local (EST) | Owner | Action | Assets |
|------------|-------------|-------|--------|--------|
| Feb 16 16:00 | Feb 16 11:00 | Ryan | Final smoke test: confirm Vercel landing, ZIP download, README badges | `workspace-ivory-one.vercel.app`, `pd-researcher.zip` |
| Feb 17 14:00 | Feb 17 09:00 | Ryan | Pre-load Show HN form in a pinned tab. Paste title + text, double-check external links. | `content/SHOW_HN_POST_NOW.md` |
| Feb 17 16:00 | Feb 17 11:00 | Ryan | Submit Show HN. Immediately post first comment (origin story or key insight) to seed discussion. | `content/show_hn_response_bank.md` |
| Feb 17 16:15–18:00 | Feb 17 11:15–13:00 | Ryan | Babysit thread every 15 min: reply to comments, log suggestions, note bugs in `memory/2026-02-17.md`. Upvote thoughtful critiques. | `content/show_hn_response_bank.md`, `content/EXECUTION_READY_SUMMARY.md` |
| Feb 17 18:00 | Feb 17 13:00 | Ryan | Publish Thread 6 "Distribution Pivot" on Twitter + LinkedIn pointing to Show HN + Vercel mirror. | `content/social_drafts.md` |
| Feb 17 19:00 | Feb 17 14:00 | Ryan | Publish Dev.to article + drop the HN link for proof. Send Console.dev + TLDR pitches referencing live traction. | `content/devto_article.md`, `content/newsletter_pitches.md` |
| Feb 17 21:00 | Feb 17 16:00 | Ryan | Push newsletter update (email_newsletter.md Email #1) summarizing hit metrics + CTA to star. | `content/email_newsletter.md` |
| Feb 18 15:00 | Feb 18 10:00 | Ryan | Post r/commandline (Template 1). Mention Show HN reception + link to response bank. | `content/reddit_posting_schedule.md` |

## 🧭 Engagement Cadence (First 6 Hours)
1. **0–60 min:** Instant replies. Capture every question + bug report. Tag follow-ups in `memory/2026-02-17.md`.
2. **60–180 min:** Rotate between HN comments and X/LinkedIn DMs. Drop clarifying comments (performance, licensing, monetization) using pre-written answers.
3. **180–360 min:** Start “what’s next” narrative — highlight affiliate approvals and upcoming directories.

When in doubt, borrow copy from `content/show_hn_response_bank.md`.

## 📊 Metrics Dashboard
Update hourly for first day (log to memory file + `content/DISTRIBUTION_DASHBOARD.md`).

| Metric | Source | Target | Notes |
|--------|--------|--------|-------|
| HN Upvotes | news.ycombinator.com | 200 (min), 400 (stretch) | Screenshot front-page placement for later case studies. |
| Comments answered | Manual tally | 100% response rate | Short “ack now, follow up later” is fine. |
| GitHub Stars | GitHub UI or `gh repo view` | +250 in 24h | Pin repo to keep star button visible. |
| Zip Downloads | Vercel analytics | 1,000 | Cross-check with Plausible once hooked. |
| Email Captures | Formspree | 50+ | Mention future Pro toolkit + audit service. |

## 📣 Cross-Channel Follow-ons
- **Twitter/LinkedIn:** Use Thread 6 (Distribution Pivot) at 18:00 UTC, Thread 7 (Zero New Tools) the next morning. Link Show HN comments to prove social proof.
- **Dev.to Article:** Publish at 19:00 UTC to ride HN spike. CTA: “Join the Show HN discussion.”
- **Reddit:** Follow `content/reddit_posting_schedule.md` (Day 1 = Feb 18 r/commandline). Mention Show HN adoption statistics for credibility.
- **Directories:** Queue AlternativeTo + SaaSHub submissions on Feb 19 while HN still fresh.

## 🛡️ Contingencies
| Risk | Trigger | Response |
|------|---------|----------|
| HN post flagged/removed | Score stalls <10 after 30 min | Re-submit with alternate title: “Show HN: 59 free CLI tools with zero dependencies.” Wait 30 min to avoid rate limit. |
| GitHub throttled | Raw links return 404/429 | Point everyone to https://workspace-ivory-one.vercel.app + /pd-researcher.zip. Update top HN comment immediately. |
| Negative "reinventing the wheel" feedback | Multiple comments | Acknowledge, reiterate single-file/zero-dependency value, invite PRs. Use Response #3 in bank. |
| Bug spotted live | User posts issue | Patch locally, push fix, reply with commit hash + explanation. Document in `memory/2026-02-17.md`. |
| Traffic spike kills Vercel bandwidth | 20k+ requests/hour | Trigger `vercel deploy --prod` to new project alias (instructions in `UNBLOCK_VERCEL.md`). Have Cloudflare Pages as Tier-2 fallback. |

## ✅ Prep Checklist (Night Before)
- [ ] Confirm Show HN copy matches 59-tool messaging and Vercel links.
- [ ] Keep GitHub + Vercel tabs open and authenticated.
- [ ] Pin `content/show_hn_response_bank.md` + Launch Pack in your notes app.
- [ ] Draft first two HN comments (origin story + monetization) for instant paste.
- [ ] Set alarms at 15:45, 16:00, 16:15 UTC.

## 🗒️ Logging
- Capture every meaningful interaction (feature request, bug, partnership ask) in `memory/2026-02-17.md`.
- Summaries roll into `content/DISTRIBUTION_DASHBOARD.md` for the next engine run.

**Remember:** No new tools. All energy → distribution, replies, and leverage.
