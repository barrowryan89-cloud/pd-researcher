# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Stripe CLI: Installed (v1.35.0) - Run `stripe login` to auth.
- Vercel CLI: Installed - Run `vercel login` to auth.
- Puppeteer: Installing in ~/.openclaw/workspace/tools/puppeteer
- Ralph: Installed in `tools/ralph/` - Autonomous AI coding loop (requires Amp CLI or Claude Code to use)
- Claude Code: Installed (v2.1.39) - Command: `claude` - Anthropic's AI coding assistant
- Amp CLI: Installed (v0.0.1770783552) - Command: `amp` - Multi-model frontier coding agent

- SSH hosts and aliases
- ElevenLabs API Key: stored in .env (Quota Exceeded / Free Tier - blocks premium voices like Lowy)
- Note: User's client attempts Auto-TTS, causing billing errors on every reply.

- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
