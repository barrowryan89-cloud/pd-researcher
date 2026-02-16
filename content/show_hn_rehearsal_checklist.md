# Show HN Rehearsal Checklist (Feb 2026)

> **Purpose:** Dry run the entire Show HN experience before the February 17 window so moderators, volunteers, and Ryan can see receipts. Follow this script every time you rehearse and log proof in `content/distribution_receipts.md`.

---

## 1. Pre-Flight (5 minutes)
- [ ] **Sync assets** — run `vercel deploy` or `npm run deploy` if you changed `index.html`, then grab the fresh hero screenshot + OG image for `assets/receipts/`.
- [ ] **Verify mirrors** — confirm the GitHub repo, Vercel landing page, and direct ZIP all load in an incognito window.
- [ ] **Open macros** — keep the following tabs ready: `content/SHOW_HN_POST_NOW.md`, `content/show_hn_response_bank.md`, `content/affiliate_comment_macros.md`.
- [ ] **Timer ready** — set a 15-minute repeating timer (phone or browser) to mimic the reply cadence during the real launch.
- [ ] **Logging sheet** — open `content/distribution_receipts.md` to note the rehearsal timestamp + proof links.

## 2. Launch Simulation (15 minutes)
1. **Post draft privately** — paste the Show HN title/body into a private note, confirm tool count + mirror URLs are correct.
2. **First-comment rehearsal** — drop the "Mirrors" first comment from README into a doc, confirm spacing, and ensure monetization disclosure is present.
3. **Response drills** — pick three common skeptic prompts (privacy, business model, affiliates) and practice responding using the macros. Record the exact snippets you used so they are copy/paste ready on launch day.
4. **Affiliate insert** — rehearse adding one contextual affiliate CTA (DigitalOcean, 1Password, Render) inside a skeptic reply so it feels natural.
5. **Directory CTA** — craft a one-line reminder pointing folks to the directory submission forms so volunteers can keep feeding the scoreboard.

## 3. Post-Rehearsal Wrap (10 minutes)
- [ ] **Capture proof** — screenshot the mock Show HN post + first comment + one rehearsal reply. Save to `assets/receipts/` (e.g., `show-hn-rehearsal-2026-02-15.png`).
- [ ] **Update README** — in the "Distribution Receipts" block, add a new bullet summarizing what you rehearsed and where proof lives.
- [ ] **Log receipts** — add a row to `content/distribution_receipts.md` with the UTC time, "Show HN rehearsal", and the screenshot filename/drive link.
- [ ] **Note blockers** — if anything felt clunky (broken link, missing macro, timer issue), document it under **Follow-Ups** below so the war room can fix it within 12 hours.

## 4. Follow-Ups
Use this table to capture issues uncovered during rehearsal.

| Date | Issue | Owner | Fix ETA | Notes |
|------|-------|-------|---------|-------|
| _(add row)_ | | | | |

---

### Quick Links
- Primary brief: `content/SHOW_HN_POST_NOW.md`
- Reply macros: `content/show_hn_response_bank.md`
- Rehearsal proof log: `content/distribution_receipts.md`
- Landing page: https://workspace-ivory-one.vercel.app
- README scoreboard: root `README.md`

Run this rehearsal once per day until launch. The muscle memory makes the real thread feel automatic and gives us receipts when moderators ask how prepared we are.