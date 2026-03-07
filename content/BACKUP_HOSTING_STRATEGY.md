# 🌐 Backup Hosting Strategy — GitHub Pages Down

**Status:** GitHub account suspended → Pages 404  
**Impact:** Landing page inaccessible, affiliate applications blocked  
**Solution:** Deploy to Vercel/Netlify as backup  
**Time to deploy:** 15 minutes  
**Cost:** $0

---

## 🚀 RECOMMENDED: Vercel Deployment

### Why Vercel
- Zero config for static sites
- GitHub integration (but can deploy without)
- Custom domains free
- Fastest global CDN
- Serverless functions if needed later

### Step-by-Step Deployment

**Option A: CLI Deploy (Fastest — No GitHub needed)**

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login (creates account if needed)
vercel login

# 3. Deploy current directory
cd /home/barrowryan89/.openclaw/workspace
vercel --prod

# 4. Get URL (e.g., pd-researcher.vercel.app)
# 5. Add custom domain later (free on Vercel)
```

**Option B: Manual Upload (No CLI needed)**

1. Go to https://vercel.com/new
2. Click "Upload" instead of importing Git
3. Drag/drop workspace folder
4. Deploy instantly
5. Get URL

---

## 🌊 Alternative: Netlify Drop

**Even simpler — no account needed**

1. Go to https://app.netlify.com/drop
2. Drag/drop workspace folder
3. Get instant URL (random-name.netlify.app)
4. Claim site with email to keep it

---

## 📋 WHAT TO DEPLOY

**Required files:**
- `index.html` (landing page)
- `install.sh` (install script)
- `og-image.png` (social preview)
- `CNAME` (if using custom domain)

**Optional:**
- `tools/` folder (for direct downloads)
- `docs/` folder (documentation)

**Total size:** ~5MB

---

## 🎯 DEPLOYMENT CHECKLIST

### Pre-Deploy (5 min)
- [ ] Update index.html: 54 → 98 tools (search/replace)
- [ ] Verify install.sh URL references
- [ ] Check og-image.png exists

### Deploy (5 min)
- [ ] Run `vercel --prod` OR use Netlify Drop
- [ ] Copy the deployed URL
- [ ] Test the site loads

### Post-Deploy (5 min)
- [ ] Update affiliate applications with new URL
- [ ] Update social drafts with new URL
- [ ] Update MEMORY.md with new URL
- [ ] Share new URL with Ryan

---

## 🔧 UPDATING INDEX.HTML FOR DEPLOY

Current issues to fix before deploy:

```bash
# Fix all "54" references to "98"
sed -i 's/54 Free CLI Tools/98 Free CLI Tools/g' index.html
sed -i 's/54 free CLI tools/98 free CLI tools/g' index.html
sed -i 's/54 single-file/98 single-file/g' index.html
sed -i 's/and 50 more/and 94 more/g' index.html

# Fix Schema.org JSON
sed -i 's/"54 free command-line tools/"98 free command-line tools/g' index.html
```

Or manually edit these lines:
- Line 5: `<title>54 Free CLI Tools...` → `<title>98 Free CLI Tools...`
- Line 6: `content="54 free CLI tools...` → `content="98 free CLI tools...`
- Line 12: `content="54 Free CLI Tools...` → `content="98 Free CLI Tools...`
- Line 13: `content="54 single-purpose...` → `content="98 single-purpose...`
- Line 19: `content="54 Free CLI Tools...` → `content="98 Free CLI Tools...`
- Line 20: `content="54 single-purpose...` → `content="98 single-purpose...`
- Line 37: `"54 free command-line tools...` → `"98 free command-line tools...`
- Line 80: `<h1>54 Free CLI Tools</h1>` → `<h1>98 Free CLI Tools</h1>`

---

## 📊 URL STRATEGY

### Immediate (Today)
Deploy to: `pd-researcher.vercel.app`

### Short-term (This Week)
- Set up custom domain: `tools.sandstreet.io` or `pdresear.ch`
- Update all links
- Redirect old GitHub Pages URL

### Long-term (When GitHub Unblocked)
- Keep Vercel as primary (faster)
- Or: GitHub Pages as primary, Vercel as backup
- Both sync from same repo

---

## 💰 BUSINESS IMPACT

| Factor | Current (404) | With Backup Host |
|--------|--------------|------------------|
| Landing page | ❌ Down | ✅ Live |
| Affiliate apps | ❌ Blocked | ✅ Can apply |
| Social posts | ❌ Can't share | ✅ Ready to post |
| Show HN | ❌ Can't submit | ✅ Ready |
| Product Hunt | ❌ Blocked | ✅ Can schedule |
| **Est. revenue loss/day** | **$13-32** | **$0** |

---

## 🚀 DEPLOY NOW — COPY/PASTE

```bash
cd /home/barrowryan89/.openclaw/workspace

# Fix the 54 -> 98 references first
sed -i 's/54 Free/98 Free/g' index.html
sed -i 's/54 free/98 free/g' index.html
sed -i 's/54 single/98 single/g' index.html

# Deploy to Vercel
npx vercel --prod

# Or use Netlify Drop (even easier)
# Go to https://app.netlify.com/drop and upload this folder
```

---

## ✅ POST-DEPLOY ACTIONS

Once live:

1. **Update affiliate applications** with new URL
2. **Submit Show HN** — content ready in `content/SHOW_HN_COPY_PASTE.txt`
3. **Post to Reddit** — drafts ready in `content/social_drafts.md`
4. **Apply to Product Hunt** — schedule for next Tuesday
5. **Update MEMORY.md** with new live URL

---

## 📁 FILES TO VERIFY

| File | Purpose | Status |
|------|---------|--------|
| `index.html` | Landing page | ⚠️ Needs 54→98 fix |
| `install.sh` | Install script | ✅ Ready |
| `og-image.png` | Social preview | ✅ Ready |
| `tools/` | 98 Python tools | ✅ Ready |

---

**Recommendation:** Deploy to Vercel in the next 15 minutes. Unblocks all distribution efforts immediately.

---

*Generated by PD Autonomous Promotion Engine — Engine Run #13*
