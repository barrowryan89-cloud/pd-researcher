# Reddit Posting Strategy

## Why Reddit

Reddit drives high-quality developer traffic:
- r/webdev: 1.1M subscribers
- r/programming: 5.8M subscribers  
- r/commandline: 400K subscribers
- Developers trust Reddit recommendations
- Long-tail traffic (posts rank in Google)

## Subreddit Analysis

### Tier 1: Primary Targets

#### r/webdev (1.1M members)
- **Best days:** Monday, Tuesday
- **Best times:** 8-10 AM EST
- **Content style:** Practical, saves money/time
- **Allowed:** Showoff Saturdays (projects allowed)
- **Risk:** Self-promo rules strict
- **Strategy:** Position as "resource share" not self-promo

#### r/programming (5.8M members)
- **Best days:** Tuesday, Wednesday
- **Best times:** 9-11 AM EST
- **Content style:** Technical, interesting implementations
- **Allowed:** Projects with technical discussion
- **Risk:** High scrutiny, must be technically substantive
- **Strategy:** Focus on "zero dependency" architecture

#### r/commandline (400K members)
- **Best days:** Any weekday
- **Best times:** 10 AM - 2 PM EST
- **Content style:** Tools, workflows, tips
- **Allowed:** Tool showcases (this is THE subreddit for us)
- **Risk:** Low — this is our perfect audience
- **Strategy:** Lead with this subreddit (highest conversion)

### Tier 2: Secondary Targets

#### r/selfhosted (600K members)
- **Angle:** "Self-hosted alternatives to SaaS tools"
- **Best content:** Cost savings, privacy benefits

#### r/coolgithubprojects (100K members)
- **Angle:** Direct project showcase
- **Best content:** GitHub link + demo

#### r/coding (150K members)
- **Angle:** Learning resource
- **Best content:** "What I learned building 98 tools"

#### r/learnprogramming (6M members)
- **Angle:** Educational resource
- **Best content:** Code examples, explanations
- **Caution:** No self-promo — focus on educational value

## Post Templates

### Template 1: r/commandline (HIGHEST PRIORITY)

```
Title: I built 98 single-file CLI tools — zero dependencies, just curl & run

Hey r/commandline,

I was tired of installing 500MB npm packages for simple tasks, so I built my own CLI tool collection.

98 tools. Single files. Zero dependencies. Most work with just curl + pipe to bash/python.

My daily drivers:
- json-fix — Validate/beautify JSON without leaving terminal
- port-kill — Kill processes by port (saves me 5min daily)
- git-todo — Task tracking embedded in git
- epoch-now — Timestamp conversions
- cloud-audit — List all AWS/GCP resources in one command

Everything is open source: https://github.com/barrowryan89-cloud/pd-researcher

The tools are intentionally simple (most under 100 lines) so you can audit and modify them easily. No black boxes.

What repetitive terminal task should I build a tool for next?
```

### Template 2: r/webdev (Cost-Saving Angle)

```
Title: I replaced $200/mo in SaaS subscriptions with open-source CLI tools

Hey r/webdev,

As an indie dev, subscription fatigue is real. I counted 23 monthly SaaS charges last month — $237 total. For things that should be simple utilities.

So I went on a 48-hour coding binge and built replacements.

The collection now has 98 CLI tools covering:
- JSON/XML processing
- Git workflows  
- Deployment scripts
- Productivity helpers
- DevOps automation

All open source. Zero dependencies. Free forever.

The "boring" ones get the most use:
- port-kill → Kill processes by port number
- focus-mode → Block distracting sites via hosts file
- standup-gen → Generate status updates from git logs

GitHub: https://github.com/barrowryan89-cloud/pd-researcher

If you're paying for simple CLI tools, you might find something useful here. What SaaS tool are you paying for that feels overpriced?
```

### Template 3: r/programming (Technical Angle)

```
Title: Showoff Saturday: 98 single-file CLI tools with zero dependencies

I challenged myself to build as many useful CLI tools as possible in 48 hours with one constraint: each tool must be a single file with zero external dependencies.

Why this constraint?
- Forces focus on the essence
- Eliminates supply chain attack surface
- Makes code auditable in minutes
- Zero install friction (curl | python3)

Tech split:
- 40% Go (speed-critical tools)
- 35% Python (data/text processing)
- 25% Bash (git/system integration)

Some interesting implementations:
- json-fix: Streaming JSON parser (no json module)
- cloud-audit: Multi-provider AWS/GCP resource lister
- secret-scan: Entropy-based secret detection

Repo: https://github.com/barrowryan89-cloud/pd-researcher

The code is intentionally simple — production code would have error handling, but these work for 95% of use cases. Perfect for learning or forking.

What would you build differently?
```

### Template 4: r/selfhosted (Privacy/Cost Angle)

```
Title: [OC] 98 self-hosted CLI alternatives to SaaS developer tools

Hey r/selfhosted,

I built a collection of CLI tools to replace SaaS subscriptions. All single files, zero dependencies, run entirely locally.

Categories:
- JSON validators/formatters (replace online tools)
- Cloud resource auditors (no third-party access)
- Secret scanners (local file analysis)
- Deployment helpers (self-hosted CI/CD)

No accounts. No data leaves your machine. No subscription fees.

Repo: https://github.com/barrowryan89-cloud/pd-researcher

What developer SaaS tools are you looking to self-host?
```

## Posting Schedule

### Week 1
- **Monday 9 AM:** r/commandline (primary launch)
- **Wednesday 10 AM:** r/webdev (if Monday performs well)

### Week 2
- **Tuesday 9 AM:** r/programming (Showoff Saturday template adjusted for day)
- **Thursday 11 AM:** r/selfhosted

### Week 3
- **Monday 9 AM:** r/coolgithubprojects
- **Wednesday 2 PM:** r/commandline (different angle — "top 10 tools")

### Week 4
- **Tuesday 10 AM:** r/coding (learning/educational angle)

## Comment Engagement Strategy

When people comment:
1. **Respond within 1 hour** (Reddit rewards engagement)
2. **Answer technical questions** thoroughly
3. **Ask follow-up questions** to drive discussion
4. **DM interested users** with specific tool recommendations
5. **Edit post** with "Edit: Thanks for the response! Here are the most requested features..."

## Anti-Spam Precautions

- **Account age:** Ensure account > 30 days old
- **Karma:** Minimum 100 karma recommended
- **Ratio:** For every self-promo post, make 5+ genuine comments
- **Cross-posting:** Don't cross-post to multiple subs same day
- **Delete & repost:** Never. Reddit detects this.

## Success Metrics

| Subreddit | Expected Upvotes | Expected Comments | Traffic |
|-----------|-----------------|-------------------|---------|
| r/commandline | 200-500 | 50-100 | 800-1,500 |
| r/webdev | 100-300 | 30-80 | 500-1,000 |
| r/programming | 50-200 | 20-60 | 300-800 |
| r/selfhosted | 100-250 | 25-50 | 400-800 |

**Total expected:** 2,000-4,100 visitors from Reddit

## Response Templates

### For "Why not just use X?"

```
Great question! A few reasons:
1. Zero dependencies = auditable in minutes
2. No install friction (curl | python3)
3. Customizable — fork and modify for your workflow
4. Learning value — see how simple tools work

That said, if X works for you, keep using it! These are alternatives, not replacements for battle-tested tools.
```

### For "This is self-promo"

```
Fair callout. I built these to solve my own problems and thought others might find them useful. Everything is free and open source — no paid tier, no upsell. Just sharing a resource.
```

### For "Tool request"

```
Love this idea! I'll add it to the list. If you want it faster, feel free to open an issue on the repo with the specific requirements.
```

---

**Status:** Posts ready to copy-paste
**Next:** Post to r/commandline first (highest conversion), wait 48h, then r/webdev
**Blocker:** GitHub Pages 404 should be fixed first (people will check the links)
