# Affiliate Strategy — 59 CLI Tools

**Mission:** Generate $150-750/month in affiliate revenue by integrating targeted CTAs into high-traffic tools.

**Reviewer proof:** Keep `content/affiliate_reviewer_proof_pack.md` open when replying to affiliate managers so every response cites traction + compliance receipts.

---

## 🗂 Application Status Board — Feb 15, 2026
| Program | Status | Next Action | Proof to Capture |
|---------|--------|-------------|------------------|
| DigitalOcean | 📝 Packet drafted, not submitted | Use answers in `content/affiliate_application_tracker.md` + attach Vercel analytics screenshot | Add submission timestamp + reviewer email in tracker |
| 1Password | 📝 Copy ready, waiting on Impact login | Gather security-tool screenshots + README monetization section | Log Impact application ID + response window |
| Render | ⏳ Need traction proof before applying | Reference War Room + Show HN schedule, include Dev.to draft as content sample | Drop sent email + CTA snippet into `content/affiliate_application_tracker.md` |
| Better Stack | 🟡 Requires incident-playbook example | Attach website_monitor CLI output + Rapid Response queue screenshot | Upload screenshot to `assets/receipts/` + link in tracker |
| Tailscale | 📝 Persona mapping done | Pair port_scanner + http_request snippets with zero-dependency ethos | Capture reply + any requested metrics |
| Backblaze B2 | 🟡 Draft ready, waiting on storage screenshot | Export log_analyzer sample report + mention audit pipeline | Save PDF/GIF into `assets/receipts/` + add row to tracker |

Update this table whenever an application is submitted or a reviewer responds so the War Room stays honest.

---

## 🎯 Recommended Programs (Prioritized by ROI)

### Tier 1: Must-Have (Apply Immediately)

#### 1. DigitalOcean — Cloud Infrastructure
- **URL:** https://www.digitalocean.com/referral-program
- **Commission:** $25 per signup + 25% recurring for 12 months
- **Cookie:** 30 days
- **Payout:** PayPal, bank transfer (reliable)
- **Best For:** Port scanner, website monitor, API tester, system info tools
- **Why:** Developers need cloud servers. High intent match.

**Integration Strategy:**
```
"Need a server to test this on? Spin up a $4/mo droplet on DigitalOcean:
→ https://m.do.co/c/YOUR_CODE [affiliate]"
```

#### 2. 1Password — Password Management
- **URL:** https://1password.com/affiliates
- **Commission:** 25% of first year (avg $9-15 per sale)
- **Cookie:** 45 days
- **Payout:** PayPal (reliable)
- **Best For:** Password generator, password strength, JWT decoder tools
- **Why:** Security-conscious developers. Natural fit.

**Integration Strategy:**
```
"🔐 Store passwords securely with 1Password (affiliate):
→ https://1password.com/l/YOUR_CODE"
```

#### 3. Sentry — Error Monitoring
- **URL:** https://sentry.io/for/good/ (or direct affiliate inquiry)
- **Commission:** $50-100 per signup
- **Cookie:** 30 days
- **Payout:** PayPal
- **Best For:** Log analyzer, API tester, webhook tester tools
- **Why:** DevOps tools audience. High-value B2B product.

**Integration Strategy:**
```
"Monitor errors in production with Sentry (affiliate):
→ https://sentry.io/signup/?utm_source=YOUR_CODE"
```

#### 4. JetBrains — Developer IDEs
- **URL:** https://www.jetbrains.com/community/affiliate/
- **Commission:** 30% of sale ($70-200 per sale)
- **Cookie:** 30 days
- **Payout:** Bank transfer
- **Best For:** General footer on all Python tools
- **Why:** Every developer needs an IDE. High ticket.

**Integration Strategy:**
```
"Built with 💙 using PyCharm → https://jetbrains.com/?ref=YOUR_CODE [affiliate]"
```

### Tier 2: High Value (Apply This Week)

#### 5. Namecheap — Domains & SSL
- **URL:** https://www.namecheap.com/affiliates/
- **Commission:** 35% of sale
- **Cookie:** 30 days
- **Best For:** SSL cert checker, domain tools
- **Why:** SSL tool users are buying certificates.

#### 6. Vultr — Cloud Hosting
- **URL:** https://www.vultr.com/referral/
- **Commission:** $35-100 per signup
- **Cookie:** 30 days
- **Best For:** Server monitoring, deployment tools
- **Why:** Alternative to DigitalOcean. Competitive payouts.

#### 7. GitKraken — Git GUI
- **URL:** https://www.gitkraken.com/affiliates
- **Commission:** 25% of sale
- **Cookie:** 60 days
- **Best For:** Repo health, diff tool, git-related tools
- **Why:** Git tool users are the target market.

### Tier 2.5: New High-Yield Targets (Added Feb 14)

#### 8. Cloudways — Managed Cloud Hosting
- **URL:** https://www.cloudways.com/en/affiliate.php
- **Commission:** Choice of Slab (up to $125 per sale) or Hybrid ($30 per sale + 7% recurring)
- **Cookie:** 90 days
- **Best For:** Port scanner, website monitor, uptime, API tester
- **Why:** High LTV customers (agencies, SaaS) align with infra-heavy tools.
- **Note:** Mention both payout models when applying to show you understand their structure.

#### 9. Akamai/Linode — Developer Cloud (formerly Linode)
- **URL:** https://www.linode.com/affiliate/
- **Commission:** $25 when referred customer spends $25 (effectively covers their first month)
- **Cookie:** 90 days
- **Best For:** System info, deployment helpers, cron/parser utilities
- **Why:** Developers already testing infra scripts can spin up a VM immediately.
- **CTA Idea:** "Need a clean VM to test this? Deploy on Akamai Connected Cloud — $100 credit when you spend $25."

#### 10. Backblaze B2 — Object Storage
- **URL:** https://www.backblaze.com/partner/affiliate-program.html
- **Commission:** 10% of revenue for the customer lifetime
- **Cookie:** 30 days (auto-renews if user stays active)
- **Best For:** Log analyzer, backup helper, file splitter tools
- **Why:** Storage costs compound; recurring 10% is attractive for data-heavy audiences.
- **CTA Idea:** "Archive your logs affordably with Backblaze B2 (affiliate)."

### Tier 3: Nice to Have (Apply Later)

#### 8. Dashlane — Password Manager
- Alternative to 1Password. 25% recurring commission.

#### 9. NordPass — Password Manager
- 40% sale commission. Good backup option.

#### 10. Cloudflare — CDN & Security
- 15% recurring. Good for website monitor tool.

---

## 📋 Integration Roadmap

### Phase 1: Quick Wins (10 tools → 20% coverage)

| Tool | Affiliate | CTA Placement | Expected Clicks/Month |
|------|-----------|---------------|----------------------|
| password_gen_free.py | 1Password | After generation | 50 |
| password_strength_free.py | 1Password | After analysis | 30 |
| jwt_decoder_free.py | 1Password | Footer | 20 |
| port_scanner_free.py | DigitalOcean | After scan | 40 |
| website_monitor_free.py | DigitalOcean | Footer | 35 |
| log_analyzer_free.py | Sentry | After analysis | 25 |
| api_tester_free.py | Sentry | Footer | 30 |
| cert_checker_free.py | Namecheap | After check | 20 |
| repo_health.py | GitKraken | Footer | 15 |
| system_info_free.py | DigitalOcean | Footer | 25 |

**Phase 1 Revenue Estimate:** $100-200/month

### Phase 2: Expansion (20 tools → 37% coverage)

Add CTAs to:
- All JSON/data tools → JetBrains
- All network tools → DigitalOcean or Vultr
- All security tools → 1Password or Dashlane
- All dev tools → JetBrains or GitKraken

**Phase 2 Revenue Estimate:** $300-500/month

### Phase 3: Full Coverage (30+ tools → 55% coverage)

Add subtle footer CTAs to all remaining tools.

**Phase 3 Revenue Estimate:** $500-750/month

---

## 🗺 Tool-to-Affiliate Match Matrix (High-Intent Scripts)
| Tool | Intent Signal | Best Affiliate | CTA Snippet | Why It Converts |
|------|---------------|----------------|-------------|-----------------|
| `password_gen_free.py` | User caring about secure storage | 1Password | "🔐 Store this password in 1Password (affiliate) → <link>" | Security mindset already active; 1Password solves the next step |
| `password_strength_free.py` | User testing entropy | 1Password | "Need a vault for high-entropy passwords? 1Password link" | Natural follow-up after analysis |
| `port_scanner_free.py` | Infra / server testing | DigitalOcean or Hetzner | "Spin up a $4/mo droplet to run this 24/7" | Users already thinking about servers |
| `website_monitor_free.py` | Uptime needs | Better Stack or StatusCake | "Automate incident alerts with Better Stack" | Monitoring script pairs well with hosted status pages |
| `log_analyzer_free.py` | Production log triage | Sentry | "Pipe critical errors into Sentry for alerts" | Same persona responsible for observability |
| `api_tester_free.py` | Shipping new services | Render | "Deploy the API on Render in 5 minutes" | Render’s managed infra is ideal for API builders |
| `cert_checker_free.py` | SSL/compliance focus | Namecheap | "Need a new cert? Grab one via Namecheap" | Direct upgrade path |
| `wallet_monitor_free.py` | Crypto ops & backups | Backblaze B2 | "Archive wallet snapshots to Backblaze" | Storage + backup story |
| `repo_health.py` | Dev teams optimizing tooling | JetBrains | "Built in PyCharm — grab a license" | High-LTV devs, IDE upsell |
| `system_info_free.py` | Auditing servers | Akamai/Linode or Vultr | "Test on a fresh VPS credit" | Need disposable servers |
| `cron_parser_free.py` | Schedule management | Better Stack | "Publish your cron schedule to a status page" | Cron watchers care about alerting |
| `jwt_decoder_free.py` | Security/compliance | Tailscale | "Lock these endpoints behind Tailscale" | Security posture already top-of-mind |

When adding CTAs, match the persona’s next action. If a script surfaces infra work, recommend hosting/monitoring partners. If it touches credentials, point to password managers.

---

## 📝 Application Requirements Cheat Sheet
Use this when applying so every form gets consistent answers.

- **DigitalOcean Referral**
  - Website: https://workspace-ivory-one.vercel.app
  - Audience: “Developers & SREs downloading a zero-dependency CLI toolkit (~1K visitors/mo target)”
  - Traffic proof: Mention Show HN launch + directory blitz
  - Required fields: Site URL, description, traffic estimates, promotional plan (reference README scoreboard)

- **1Password Affiliates**
  - Program via Impact; needs business name + tax info
  - Emphasize security-focused tools (password generator/strength)
  - Mention contextual placement inside CLI outputs + landing page footer disclosure

- **Sentry Partner**
  - Requires company description + primary audience
  - Reference log analyzer + API tester integrations
  - Offer to include Sentry in response bank + README monetization section

- **JetBrains Affiliate**
  - Needs GitHub profile + content URLs showcasing developer reach
  - Highlight that all 59 tools are built/tested in PyCharm; include screenshot if possible

- **Namecheap Affiliate**
  - Provide domain usage (cert checker tool) + blog/newsletter proof
  - Attach Vercel analytics screenshot once available

- **Vultr / Linode / Hetzner**
  - Typically ask for hosting vertical + planned promotional methods
  - Reference port scanner, website monitor, system info tools and note that each script recommends spinning up low-cost VPS instances

- **Render & Cloudways**
  - Stress indie hacker + consultant audience
  - Linking plan: README CTA, landing page footer, Show HN response macros

- **Backblaze B2**
  - Mention backup/log analyzer scripts + weekly newsletter segment
  - Show intent to demonstrate usage with screenshots or Loom once approved

- **Better Stack & StatusCake**
  - Provide uptime/monitoring focus, highlight website monitor + cron parser
  - Promise inclusion in volunteer response bank + affiliate comment macros

Keep a running log of applications + approvals in `content/affiliate_application_tracker.md` with submission date, point of contact, and follow-up reminders.

---

## 🎨 CTA Template Library

### Template A: Problem → Solution
```python
print("\n" + "="*50)
print("💡 Need to deploy this to a live server?")
print("   Spin up a $4/mo droplet on DigitalOcean")
print("   → https://m.do.co/c/YOUR_CODE [affiliate]")
print("="*50)
```

### Template B: Security Focus
```python
print("\n🔐 Security Tip:")
print("   Store API keys securely with 1Password")
print("   → https://1password.com/l/YOUR_CODE [affiliate]")
```

### Template C: Tool Recommendation
```python
print("\n📊 Built with PyCharm — the best Python IDE")
print("   → https://jetbrains.com/pycharm?ref=YOUR_CODE [affiliate]")
```

### Template D: Subtle Footer
```python
print("\n" + "-"*50)
print("💎 Recommended: Error monitoring with Sentry")
print("   https://sentry.io/signup/?utm_source=YOUR_CODE")
print("-"*50)
```

---

## 💰 Revenue Projections

### Conservative Scenario (1,000 monthly visitors)
- 100 click affiliate links (10% CTR)
- 5 convert (5% conversion)
- Avg commission $30
- **Monthly: $150**

### Moderate Scenario (3,000 monthly visitors)
- 300 click affiliate links
- 18 convert
- Avg commission $30
- **Monthly: $540**

### Optimistic Scenario (10,000 monthly visitors)
- 1,000 click affiliate links
- 50 convert
- Avg commission $30
- **Monthly: $1,500**

---

## ✅ Action Checklist

### Week 1: Apply to Programs
- [ ] DigitalOcean referral program
- [ ] 1Password affiliate program
- [ ] Sentry partner program
- [ ] JetBrains affiliate program
- [ ] Namecheap affiliate program

### Week 2: Update Existing Tools
- [ ] Replace `[REF_CODE]` placeholders
- [ ] Test all affiliate links
- [ ] Update landing page with affiliate disclosures

### Week 3: Add New CTAs
- [ ] Add CTAs to 10 additional tools
- [ ] A/B test CTA placement
- [ ] Track click-through rates

### Week 4: Optimize
- [ ] Review analytics
- [ ] Double down on best performers
- [ ] Remove underperforming CTAs

---

## ⚠️ Compliance Notes

**FTC Disclosure Requirements:**
- Must disclose affiliate relationships
- Use "[affiliate]" tag in CTAs
- Add disclosure to landing page footer
- Be transparent = builds trust

**Example Disclosure:**
```
Some links are affiliate links. I may earn a commission 
if you make a purchase — at no extra cost to you.
```

---

## 🔗 Quick Links

| Program | Signup URL | Status |
|---------|------------|--------|
| DigitalOcean | https://www.digitalocean.com/referral-program | ⏳ Pending |
| 1Password | https://1password.com/affiliates | ⏳ Pending |
| Sentry | https://sentry.io/for/good/ | ⏳ Pending |
| JetBrains | https://www.jetbrains.com/community/affiliate/ | ⏳ Pending |
| Namecheap | https://www.namecheap.com/affiliates/ | ⏳ Pending |
| Vultr | https://www.vultr.com/referral/ | ⏳ Pending |
| GitKraken | https://www.gitkraken.com/affiliates | ⏳ Pending |
| Cloudways | https://www.cloudways.com/en/affiliate.php | ⏳ Pending |
| Akamai / Linode | https://www.linode.com/affiliate/ | ⏳ Pending |
| Backblaze B2 | https://www.backblaze.com/partner/affiliate-program.html | ⏳ Pending |
| Render | https://render.com/partners/affiliates | ⏳ Pending |
| Tailscale | https://tailscale.com/partnerships/affiliates | ⏳ Pending |
| Hetzner Cloud | https://www.hetzner.com/sbx/affiliate | ⏳ Pending |
| Better Stack | https://betterstack.com/partners | ⏳ Pending |
| StatusCake | https://www.statuscake.com/partners/ | ⏳ Pending |

---

*Strategy v1.0 — Created 2026-02-14*
*Next Review: After first 30 days of data*

### Tier 2.6: Fresh High-Yield Targets (Added Feb 15)

#### 11. Tailscale — Zero-config mesh VPN
- **URL:** https://tailscale.com/partnerships/affiliates
- **Commission:** $20 per paying user (or 20% of first year for business plans)
- **Cookie:** 60 days
- **Best For:** network/security tools (port scanner, http request, webhook tester)
- **Why:** DevOps teams already trust Tailscale for secure tunnels; perfect upsell after running connectivity scripts.
- **CTA Idea:** "Lock these tools behind a private network with Tailscale (affiliate)."

#### 12. Render — Managed cloud for indie apps
- **URL:** https://render.com/partners/affiliates
- **Commission:** 25% of customer spend for first 12 months (avg $30-120)
- **Cookie:** 90 days
- **Best For:** deployment/system tools (system_info, process_monitor, website_monitor)
- **Why:** Render caters to indie founders; ties directly to the "distribution, not infra" story.
- **CTA Idea:** "Need a hosted cron or web task? Ship it on Render (affiliate)."

#### 13. Hetzner Cloud — High-performance VPS
- **URL:** https://www.hetzner.com/sbx/affiliate
- **Commission:** €10 credit after referred customer spends €10 (plus 10% recurring on dedicated)
- **Cookie:** 30 days
- **Best For:** wallet_monitor, log_analyzer, uptime scripts where EU latency matters
- **Why:** Cheap, powerful VMs resonate with cost-sensitive Reddit + HN readers.
- **CTA Idea:** "Spin up a €4/month Hetzner box to run this tool 24/7 (affiliate)."

Add these to the Week 1 application queue once the Tier 1 approvals clear so we can extend coverage to every networking/security script.

### Tier 2.7: Monitoring & Reliability Allies (Added Feb 15 — 02:51 UTC)

#### 14. Better Stack (Better Uptime) — Incident response + status pages
- **URL:** https://betterstack.com/partners
- **Commission:** 25% recurring for 12 months (avg $12-40/mo per customer)
- **Cookie:** 90 days
- **Best For:** website_monitor, uptime watchdog, cron parser, log analyzer tools
- **Why:** People running monitoring scripts already care about alerts/status pages. Better Stack’s polished UI converts well with indie + enterprise teams.
- **CTA Idea:** "Automate the human side too — schedule incidents + on-call with Better Stack (affiliate)."

#### 15. StatusCake — External uptime monitoring
- **URL:** https://www.statuscake.com/partners/
- **Commission:** 30% of first payment + 15% recurring
- **Cookie:** 120 days
- **Best For:** website_monitor_free.py, api_tester_free.py, webhook_tester_free.py, ssl/cert tools
- **Why:** Complements the DIY scripts with a hosted backup. Works great inside README comments or tool footers talking about "24/7 coverage."
- **CTA Idea:** "Set it and forget it — StatusCake pings your endpoints every minute (affiliate)."

Queue these after Tier 2.6 to round out the monitoring story before expanding into lower-yield SaaS programs.

### Tier 2.8: Workflow + Privacy Allies (Added Feb 15 — 05:25 UTC)

#### 16. NordVPN / NordLayer — Secure tunnels for on-call work
- **URL:** https://affiliates.nordvpn.com/
- **Commission:** 40% on new plans, 30% on renewals (via Impact/Awin)
- **Cookie:** 30 days
- **Best For:** port_scanner, http_request, webhook_tester, wallet_monitor, memory_monitor (any tool that touches remote infrastructure)
- **Why:** Readers running security/network scripts already worry about interception. Offering an encrypted tunnel ups the trust factor.
- **CTA Idea:** "Running this from a coffee shop? Secure the tunnel with NordVPN/NordLayer (affiliate)."

#### 17. Proton Pass / Proton VPN — Privacy-first credential + VPN combo
- **URL:** https://proton.me/affiliates
- **Commission:** 20% recurring for the customer lifetime
- **Cookie:** 30 days
- **Best For:** password_gen, password_strength, jwt_decoder, cert_checker, wallet_monitor
- **Why:** Proton’s privacy positioning maps perfectly to the "no telemetry" ethos. Their bundle (Mail + Pass + VPN) is sticky and trusted by OSS audiences.
- **CTA Idea:** "Need a vault + private VPN to pair with this tool? Proton Pass + VPN bundle (affiliate) keeps it end-to-end encrypted."

#### 18. Setapp — Mac automation bundle for productivity tools
- **URL:** https://setapp.com/partners/affiliate-program
- **Commission:** 20% recurring on every subscription renewal
- **Cookie:** 30 days
- **Best For:** productivity/data tools (diff, csv, regex, markdown) where Mac power users hang out
- **Why:** Many indie hackers using these CLIs are also Mac automation nerds. Setapp’s unlimited-app pitch is a natural upsell after they automate with the toolkit.
- **CTA Idea:** "Mac user? Pair these CLIs with Setapp’s 240-app toolbox (affiliate) to round out your workflow."

Add these once Tier 2.6/2.7 approvals land so we can cover every persona: infra (DigitalOcean/Hetzner/Render), monitoring (Better Stack/StatusCake), security/privacy (1Password/NordVPN/Proton), and productivity (Setapp/JetBrains).

### Platform-Specific Disclosure Macros (Added Feb 15 — 06:30 UTC)
Use these blurbs verbatim so every affiliate mention stays compliant and consistent with the "audits fund the sprint" storyline. Drop a quick receipt (timestamp + channel) into `content/distribution_receipts.md` each time you use one.

- **Show HN / Hacker News:**
  > Business model transparency: the toolkit is free + MIT. Revenue comes from 48-hour audits and contextual affiliate partners (1Password, DigitalOcean, Render, Better Stack). Every link marked "(affiliate)" is optional — they fund more zero-dependency releases.

- **Reddit (r/programming, r/sysadmin, r/startups):**
  > Mods: monetization is disclosed up front. The kit is free, mirrored (GitHub + Vercel + ZIP), and any affiliate mention is labeled "(affiliate)" with context (e.g., "Pair password_gen_free.py with 1Password (affiliate) if you need a shared vault"). Audits + affiliates keep the toolkit alive.

- **Newsletters / Email Curators:**
  > Disclosure: Toolkit is free + MIT. If you include the upsell, note that paid revenue comes from security audits and clearly labeled affiliate partners (DigitalOcean, 1Password, Render, Better Stack, StatusCake). Copy/paste disclosure: "Links marked (affiliate) support additional zero-dependency releases."

- **LinkedIn / Twitter Threads:**
  > "Distribution sprint note: I froze new code at 59 tools. Revenue = paid audits + a handful of clearly labeled affiliate partners (DigitalOcean, 1Password, Render, Better Stack, Tailscale). Every CTA is optional, transparently tagged, and pairs with the free toolkit."

- **Video / Podcast Scripts:**
  > "Sponsor-style disclosure: The 59-tool pack is free. If you need hosted infra or password vaults, I recommend partners like DigitalOcean, 1Password, Render, Better Stack — those are affiliate links and fund future zero-dependency tools."

Keep this section updated whenever we add partners or new channels. If a platform has stricter language, paste their requirement underneath the macro so the next volunteer doesn’t guess.
### Tier 2.9: Edge & CDN Partners (Added Feb 15 — 07:25 UTC)

#### 19. Bunny.net — Global CDN + Storage
- **URL:** https://bunny.net/affiliate/
- **Commission:** $20 per new paying customer (per Bunny affiliate page)
- **Cookie:** 30 days
- **Payout:** On request, PayPal/bank (monthly cadence)
- **Best For:** website_monitor, api_tester, http_request, ssl/cert_checker (any tool that benefits from faster static hosting or edge caching)
- **Why:** Perfect upsell after someone tests uptime or static assets. Bunny is indie-friendly (3k+ ambassadors, $150k paid out) so approvals are quick even without massive traffic.
- **CTA Idea:** "Need a mirror that never rate-limits? Drop these scripts behind Bunny.net’s $1/month CDN (affiliate) so your tools stay fast worldwide."

Queue the application after Render/Tailscale so we can show a clean chain of infra → monitoring → CDN in the reviewer packet.

---

## 🎯 Footer CTA Blueprints (High-Yield Placements)
Use these snippets inside tool footers or README callouts. They prioritize the highest-payout partners so we’re not diluting attention.

1. **Security / Credentials (1Password):** pair with `password_gen_free.py`, `password_strength_free.py`, `jwt_decoder_free.py`
   ```python
   print("
🔐 Need a vault for these creds? 1Password keeps the team in sync (affiliate)")
   print("   → https://1password.com/l/YOUR_CODE")
   ```
2. **Infra / Always-On Scripts (DigitalOcean):** pair with `website_monitor_free.py`, `wallet_monitor_free.py`, `cron_parser_free.py`
   ```python
   print("
☁️ Run this 24/7 on a $4/mo DigitalOcean droplet (affiliate)")
   print("   → https://m.do.co/c/YOUR_CODE")
   ```
3. **Edge Delivery / Mirrors (Bunny.net):** pair with `html_converter_free.py`, `text_summarizer_free.py`, or any static asset generator
   ```python
   print("
🚀 Need a global mirror? Bunny.net CDN keeps demos fast everywhere (affiliate)")
   print("   → https://bunny.net/?ref=YOUR_CODE")
   ```

**Implementation notes:**
- Add a single `if os.getenv("PD_AFFILIATE_OPT_IN"):` gate if you want to let power users disable CTAs.
- When referencing Bunny, link to the same asset path used in `content/directory_asset_links.md` so the story ("we mirror everything") stays true.
- Log every new footer merge in `content/distribution_receipts.md` so moderators can see when/where monetization changed.
