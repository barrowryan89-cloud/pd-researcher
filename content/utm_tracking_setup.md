# UTM Tracking & Analytics Setup

## Why UTM Matters

Without UTM parameters, all traffic looks the same. We need to know:
- Which channel drives the most GitHub stars
- Which content converts to email subscribers
- Where to double down our efforts

## UTM Structure

**Base URL:** `https://barrowryan89-cloud.github.io/pd-researcher/`
**GitHub URL:** `https://github.com/barrowryan89-cloud/pd-researcher`

### URL Builder Template

```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}&utm_content={content}
```

## Pre-Built UTM Links

### Social Media

**Twitter/X (Organic)**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=twitter&utm_medium=social&utm_campaign=tool_launch&utm_content=organic
```

**Twitter/X (Thread)**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=twitter&utm_medium=social&utm_campaign=tool_launch&utm_content=thread
```

**LinkedIn**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=linkedin&utm_medium=social&utm_campaign=tool_launch&utm_content=post
```

**Reddit r/webdev**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=reddit&utm_medium=social&utm_campaign=tool_launch&utm_content=webdev
```

**Reddit r/programming**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=reddit&utm_medium=social&utm_campaign=tool_launch&utm_content=programming
```

**Reddit r/commandline**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=reddit&utm_medium=social&utm_campaign=tool_launch&utm_content=commandline
```

### Content Platforms

**Dev.to Article**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=devto&utm_medium=content&utm_campaign=tool_launch&utm_content=article
```

**Hacker News (Show HN)**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=hackernews&utm_medium=social&utm_campaign=tool_launch&utm_content=show_hn
```

**Product Hunt**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=producthunt&utm_medium=social&utm_campaign=tool_launch&utm_content=launch
```

### Directories & Communities

**GitHub Explore**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=github&utm_medium=referral&utm_campaign=tool_launch&utm_content=explore
```

**Awesome Lists (if featured)**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=awesome_lists&utm_medium=referral&utm_campaign=tool_launch&utm_content=featured
```

**Newsletter (Console, TLDR, etc.)**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source={newsletter_name}&utm_medium=email&utm_campaign=tool_launch&utm_content=feature
```

### Email Newsletter

**Welcome Email**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=email&utm_medium=email&utm_campaign=newsletter&utm_content=welcome
```

**Weekly Digest**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=email&utm_medium=email&utm_campaign=newsletter&utm_content=digest
```

**New Tool Announcement**
```
https://github.com/barrowryan89-cloud/pd-researcher?utm_source=email&utm_medium=email&utm_campaign=newsletter&utm_content=new_tool
```

## Campaign Tracking

### Primary Campaign: `tool_launch`
Duration: Ongoing
Goal: Drive initial traffic and GitHub stars

### Future Campaigns

**`affiliate_promo`** — When affiliate links are live
**`paid_ads`** — If we test Twitter/Reddit ads
**`feature_update`** — New tools added
**`case_study`** — Success stories/testimonials

## Short Link Strategy

For platforms with character limits (Twitter), use:
- `git.new/pd-tools` → GitHub (if available)
- `pd.researcher/tools` → Landing page (custom domain)
- Or: Bitly/Short.io for trackable short links

## GitHub Traffic Insights

GitHub provides basic analytics at:
`https://github.com/barrowryan89-cloud/pd-researcher/graphs/traffic`

Shows:
- Referring sites
- Popular content
- Visitor trends

**Check weekly** to identify top traffic sources.

## Landing Page Analytics

Once GitHub Pages is fixed, add:

### Google Analytics 4 (Free)
Add to landing page `<head>`:
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Plausible (Privacy-Friendly Alternative)
```html
<script defer data-domain="barrowryan89-cloud.github.io" src="https://plausible.io/js/script.js"></script>
```

### Key Events to Track

| Event | Trigger | Why |
|-------|---------|-----|
| `view_landing` | Page load | Baseline traffic |
| `click_github` | CTA button click | Conversion to GitHub |
| `click_tool` | Tool link click | Popular tools |
| `email_subscribe` | Form submit | Lead generation |
| `scroll_depth` | 50%, 90% scroll | Content engagement |

## Expected Metrics by Channel (First 30 Days)

| Channel | Traffic | Star Conversion | Email Conversion |
|---------|---------|-----------------|------------------|
| Hacker News | 1,000 | 3-5% (30-50 stars) | 1% (10 subs) |
| Reddit | 800 | 4-6% (32-48 stars) | 1.5% (12 subs) |
| Twitter | 500 | 2-3% (10-15 stars) | 0.5% (3 subs) |
| Product Hunt | 2,000 | 5-8% (100-160 stars) | 2% (40 subs) |
| Dev.to | 1,500 | 3-4% (45-60 stars) | 1% (15 subs) |
| Direct/Other | 500 | 2% (10 stars) | 0.5% (3 subs) |

**Total Estimates:**
- Traffic: 6,300 visitors
- GitHub Stars: 227-343
- Email Subscribers: 83

## Reporting Dashboard

Create a simple tracking spreadsheet with:

| Date | Source | Medium | Visitors | Stars | Emails | Notes |
|------|--------|--------|----------|-------|--------|-------|
| 2026-02-14 | twitter | social | 150 | 5 | 2 | Thread posted 9am |
| 2026-02-14 | hackernews | social | 800 | 35 | 8 | Show HN front page 2hrs |

**Review weekly** to identify winning channels.

## Action Items

- [ ] Set up Google Analytics 4 (free)
- [ ] Add UTM links to all social drafts
- [ ] Create tracking spreadsheet
- [ ] Schedule weekly analytics review
- [ ] Set up GitHub traffic monitoring

---

**Status:** Ready to implement
**Blocker:** GitHub Pages 404 must be fixed first
**Next:** Add GA4 tag to landing page once live
