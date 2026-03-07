---
name: screenshot-reader
description: Read screenshots/images and extract text + actionable insights.
homepage: https://docs.openclaw.ai
metadata:
  {
    "openclaw": {
      "emoji": "🖼️",
      "requires": {"inputs": ["image"]}
    }
  }
---

# screenshot-reader

Use this skill when Ryan drops a screenshot (X posts, dashboards, receipts, UI screens) and wants the content read + turned into actions.

## What it does
Given an image, return:
1) **Exact extracted text** (as faithfully as possible)
2) **Summary** (1-3 sentences)
3) **Ideas / next actions** (bullet list)
4) If it’s a social post: **suggested reply + suggested quote-tweet**

## How to use (Ryan)
1) Upload a screenshot in Telegram.
2) Say what you want: "summarize", "pull ideas", "draft reply", "extract handles", etc.

## How I run it (PD)
- Use built-in vision to read the screenshot.
- If handles/links are present: normalize them to copy/paste.
- If it’s a UI flow: identify the next 3 clicks.

## Output format (default)
TEXT:
<verbatim-ish extracted text>

SUMMARY:
<short>

IDEAS / ACTIONS:
- ...

DRAFT REPLY (optional):
...

DRAFT POST (optional):
...
