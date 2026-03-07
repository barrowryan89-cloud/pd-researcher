# HOW TO FIX VERCEL 401 (Deployment Protection)

## 🚨 CRITICAL: The landing page is blocked.
Visitors see a password prompt. This MUST be fixed before posting to HN.

### Step-by-Step Fix (5 Minutes)

1. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard

2. **Select Project:**
   - Find `pd-researcher` in your list.

3. **Go to Settings:**
   - Click the "Settings" tab at the top.

4. **Deployment Protection:**
   - Find "Deployment Protection" in the sidebar.
   - Look for **"Vercel Authentication"** or **"Password Protection"**.
   - **TURN IT OFF.** (Toggle to Disabled).
   - Click "Save".

5. **Verify:**
   - Open your project URL in Incognito Mode.
   - It should load instantly without a password.

---

### If You Can't Find It:
- Sometimes it's under "Security" tab.
- Or check if you are on a Pro trial that enforces it (unlikely for Personal).
- Or delete the project and re-deploy using CLI:
  ```bash
  vercel --prod --public
  ```

### Verify Correct URL
- Once fixed, copy the *cleanest* URL (e.g., `pd-researcher.vercel.app` if available).
- Update `content/SHOW_HN_POST_NOW.md` with this URL.

**Done.**
