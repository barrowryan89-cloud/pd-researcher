# Affiliate Footer Rollout — Batch 1 (Feb 15, 2026)

**Mission:** Prioritize the highest-intent scripts for contextual affiliate CTAs so every download nudges revenue toward the $1M goal. This playbook only covers the first 10 tools so we can merge fast, measure, then expand.

## 📊 Tool → Partner Map
| Tool | Persona Signal | Affiliate Partner | Commission Snapshot | CTA Copy (drop near script footer) | Notes |
|------|----------------|-------------------|---------------------|------------------------------------|-------|
| `port_scanner_free.py` | Infra/security engineer testing hosts | DigitalOcean Referral | $25 signup bonus + 25% of first 12 months | `Run this 24/7 on a $4/mo DigitalOcean droplet (affiliate) → https://m.do.co/c/YOURCODE` | Mention mirror + ZIP for moderators; tie to uptime stories |
| `website_monitor_free.py` | SRE / ops watching uptime | Better Stack Affiliate | 25% recurring for 12 months | `Need alerts + on-call? Better Stack handles incidents (affiliate) → https://betterstack.com/partners/YOURCODE` | Pair with incident macro in README war room |
| `wallet_monitor_free.py` | Crypto ops team tracking balances | Backblaze B2 | 10% lifetime revenue | `Archive wallet snapshots in Backblaze B2 (affiliate) → https://www.backblaze.com/b2/cloud-storage.html#afid=YOURCODE` | Add reminder about encrypted backups |
| `password_gen_free.py` | Security-conscious dev saving creds | 1Password (Impact) | 25% of first year | `Store this password in 1Password (affiliate) → https://1password.com/l/YOURCODE` | Keep CTA behind `if not os.getenv("PD_NO_AFFILIATE")` to satisfy CLI purists |
| `password_strength_free.py` | Auditing existing secrets | Proton Pass / Proton VPN | 20% recurring | `Need a vault + VPN combo? Proton Pass keeps it private (affiliate) → https://proton.me/affiliates/YOURCODE` | Proton positioning = privacy-first; matches MIT ethos |
| `jwt_decoder_free.py` | API/security engineer inspecting tokens | Tailscale Partner | ~$20 per activated user | `Lock these endpoints behind Tailscale (affiliate) → https://tailscale.com/partners/YOURCODE` | Reference zero-config meshes in README for credibility |
| `log_analyzer_free.py` | DevOps parsing prod logs | Sentry Partner | $50-100 per qualified signup | `Pipe critical errors into Sentry (affiliate) → https://sentry.io/signup/?utm_source=YOURCODE` | Add same CTA to `content/show_hn_response_bank.md` when answering "how do you monetize" |
| `api_tester_free.py` | Indie founders testing services | Render Affiliate | 25% of spend for first 12 months | `Need managed cron + web services? Ship it on Render (affiliate) → https://render.com/partners/YOURCODE` | Mention “distribution sprint” so reviewers see honest monetization |
| `cron_parser_free.py` | Ops/consultant cleaning schedules | Better Stack or StatusCake | 25-30% commissions | `Offload alerting to StatusCake (affiliate) → https://www.statuscake.com/partners/YOURCODE` | Choose Better Stack OR StatusCake per region to avoid double CTAs |
| `system_info_free.py` | Sysadmins auditing servers | Akamai/Linode | $25 once user spends $25 | `Spin up a clean Linode VM ($100 credit) to run this audit (affiliate) → https://www.linode.com/affiliate/YOURCODE` | Perfect tie-in for AlternativeTo + StackShare listings

## ✅ Implementation Checklist
1. **Confirm opt-in flag:** add `AFFILIATE_OPT_IN = os.getenv("PD_AFFILIATE_OPT_IN", "1") == "1"` helper so advanced users can silence CTAs.
2. **Standardize disclosure:** append `"(affiliate)"` to every CTA + link to README disclosure once per script.
3. **Update `content/affiliate_application_tracker.md`:** record which partners are live vs pending so we don’t ship dead links.
4. **Log merges:** each time a footer ships, add an entry to `content/distribution_receipts.md` (timestamp, file, partner) for reviewer proof.
5. **A/B hooks:** start with upbeat CTA copy above; if CTR <5%, test urgency variants ("Don’t babysit cron manually...").

## 🧪 Measurement Plan
- **Clicks:** instrument via UTM tags in README + landing page (already defined in `content/utm_tracking_setup.md`).
- **Conversions:** pull Impact/PartnerStack dashboards weekly; summarize in `memory/2026-02-15.md` so Ryan has receipts.
- **Qual feedback:** watch Show HN / Reddit comments for pushback; if devs complain, gate CTAs behind `--no-affiliate` flag.

## 🚀 Next Batch Candidates
- `json_formatter_free.py` → JetBrains CTA (IDE productivity)
- `html_cleaner_free.py` → Bunny.net (edge mirror)
- `process_monitor_free.py` → Backblaze (log archiving)
- `duplicate_finder_free.py` → Backblaze (storage cleanup)
- `text_summarizer_free.py` → Setapp (Mac automation pack)

Documenting the first batch keeps us honest with moderators and speeds up future merges once approvals arrive.
