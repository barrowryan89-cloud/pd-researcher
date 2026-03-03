# LEARNINGS.md - Mistake → Rule Pipeline

**Format:** DATE | MISTAKE | ROOT CAUSE | RULE CREATED | REVIEWED?

---

## 2026-02-27 | Leaked Internal Thinking
**Mistake:** User said "stop leaking your internal thinking" - I was narrating my process instead of just delivering results.
**Root Cause:** Confused "being helpful" with "being verbose".
**Rule:** Only narrate when it adds value. Default: deliver result, then brief context if asked.
**Status:** ✅ Implemented

## 2026-02-27 | Polymarket Username Resolution
**Mistake:** Spent 8+ attempts trying to resolve usernames via API when a simple Google search found the Substack article with all addresses.
**Root Cause:** Didn't try the obvious path first (web search for the exact usernames).
**Rule:** When API fails, try web search + manual lookup before claiming it's impossible.
**Status:** ✅ Implemented

## 2026-02-26 | GitHub Suspension
**Mistake:** Pushed sensitive files (wallets, cron jobs) to GitHub, got account suspended.
**Root Cause:** No pre-push security scan. No `.gitignore` for sensitive files.
**Rule:** Run `git status` + security audit before every push. Never commit files with "wallet", "key", "secret", "password" in filename.
**Status:** ✅ Implemented

---

## TEMPLATE FOR NEW ENTRIES
```
## YYYY-MM-DD | [Brief Description]
**Mistake:** [What happened]
**Root Cause:** [Why it happened]
**Rule:** [New rule to prevent recurrence]
**Status:** [Pending/Implemented]
```

**Review Schedule:** Check at start of every session. Making same mistake twice = unforgivable.
