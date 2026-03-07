# Follow-Up Autopilot

**Stop letting leads go cold. Automate your follow-up game.**

## What It Does

Follow-Up Autopilot generates personalized follow-up message drafts and reminder schedules for any communication channel. Give it a person, context, and goal — it outputs:

- 3 message variations (short/medium/direct)
- Smart reminder schedule
- OpenClaw cron jobs for automated reminders
- Compact daily ping list

Perfect for sales follow-ups, partnership outreach, job applications, or any scenario where persistence matters.

## Installation

```bash
chmod +x tools/followup_autopilot.py
```

**Dependencies:** Python 3.7+ (standard library only)

## Usage

### Basic Usage

```bash
./tools/followup_autopilot.py \
  --person "Alex Chen" \
  --context "demo request from LinkedIn" \
  --goal "schedule 30-min product demo" \
  --channel email \
  --tone friendly \
  --timeline "1d,3d,7d"
```

### With Start Date (Absolute Scheduling)

```bash
./tools/followup_autopilot.py \
  --person "Jordan" \
  --context "pitch deck sent" \
  --goal "get feedback and next steps" \
  --channel slack \
  --tone direct \
  --timeline "2d,5d,10d" \
  --start "2026-02-11T09:00:00"
```

### JSON Input (stdin)

```bash
echo '{
  "person": "Sam Rivera",
  "context": "coffee chat follow-up",
  "goal": "intro to VP of Product",
  "channel": "text",
  "tone": "friendly",
  "timeline": "1d,4d,8d"
}' | ./tools/followup_autopilot.py --stdin
```

### JSON Output

```bash
./tools/followup_autopilot.py \
  --person "Taylor" \
  --context "contract proposal" \
  --goal "signed agreement" \
  --channel dm \
  --timeline "1d,3d,5d,7d" \
  --json
```

## Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `--person` | Yes* | Person to follow up with | - |
| `--context` | Yes* | Context of the follow-up | - |
| `--goal` | Yes* | Goal of the follow-up | - |
| `--channel` | No | Channel: email, text, dm, slack, discord | email |
| `--tone` | No | Tone: direct, friendly | friendly |
| `--timeline` | No | Follow-up schedule (e.g., 1d,3d,7d) | 1d,3d,7d |
| `--start` | No | Start date (ISO format) | now |
| `--stdin` | No | Read JSON from stdin | false |
| `--json` | No | Output as JSON | false |

\* Required unless using `--stdin`

## Output

### Human-Readable (default)

```
======================================================================
FOLLOW-UP AUTOPILOT
======================================================================

👤 Person: Alex Chen
📋 Context: demo request from LinkedIn
🎯 Goal: schedule 30-min product demo
📱 Channel: email
💬 Tone: friendly
⏱️  Timeline: +1d, +3d, +7d

======================================================================
📝 MESSAGE DRAFTS
======================================================================

[1] SHORT (~1-2 sentences)
Format: Subject line + body
──────────────────────────────────────────────────────────────────────
Hey Alex Chen! Just wanted to check in about schedule 30-min product demo 😊

[2] MEDIUM (~3-4 sentences)
Format: Subject line + body
──────────────────────────────────────────────────────────────────────
Hi Alex Chen! Hope things are going well. I wanted to follow up on demo request from LinkedIn. Any progress on schedule 30-min product demo?

[3] DIRECT (Full message)
Format: Subject line + body
──────────────────────────────────────────────────────────────────────
Hey Alex Chen!

Hope you're having a great week! I wanted to circle back on demo request from LinkedIn.

I know things get busy, but I'd love to hear any updates on schedule 30-min product demo when you get a chance.

No rush - just keeping this on the radar!

Cheers!

======================================================================
📅 REMINDER SCHEDULE
======================================================================
• 1 day after initial contact
  → 2026-02-12 at 09:00
• 3 days after initial contact
  → 2026-02-14 at 09:00
• 7 days after initial contact
  → 2026-02-18 at 09:00

======================================================================
📌 DAILY PINGS
======================================================================
📌 Day +1: Wed Feb 12
📌 Day +3: Fri Feb 14
📌 Day +7: Tue Feb 18

======================================================================
⚙️  CRON JOB SNIPPETS (OpenClaw)
======================================================================

Use with: openclaw cron add --json '<snippet>'

[1] {
  "type": "systemEvent",
  "event": "reminder",
  "schedule": "2026-02-12T09:00:00",
  "payload": {
    "title": "Follow up with Alex Chen",
    "body": "Re: demo request from LinkedIn - Goal: schedule 30-min product demo",
    "priority": "normal",
    "tags": ["follow-up", "autopilot"]
  },
  "metadata": {
    "sequence": 1,
    "total": 3,
    "person": "Alex Chen",
    "context": "demo request from LinkedIn",
    "goal": "schedule 30-min product demo"
  }
}

======================================================================
```

### JSON Output (`--json`)

```json
{
  "person": "Alex Chen",
  "context": "demo request from LinkedIn",
  "goal": "schedule 30-min product demo",
  "channel": "email",
  "tone": "friendly",
  "timeline_days": [1, 3, 7],
  "drafts": [...],
  "schedule": {...},
  "cron_jobs": [...],
  "daily_pings": [...]
}
```

## Use Cases

### Sales Follow-Ups

```bash
./tools/followup_autopilot.py \
  --person "CEO at StartupCo" \
  --context "B2B SaaS demo completed" \
  --goal "close $50k annual contract" \
  --channel email \
  --tone direct \
  --timeline "1d,3d,7d,14d"
```

### Networking

```bash
./tools/followup_autopilot.py \
  --person "Sarah (conference connection)" \
  --context "chatted about AI at TechCon" \
  --goal "virtual coffee chat" \
  --channel dm \
  --tone friendly \
  --timeline "2d,7d"
```

### Job Applications

```bash
./tools/followup_autopilot.py \
  --person "Hiring Manager" \
  --context "interview for Senior Engineer role" \
  --goal "decision and offer" \
  --channel email \
  --tone friendly \
  --timeline "3d,7d,10d"
```

### Partnership Outreach

```bash
./tools/followup_autopilot.py \
  --person "Head of Partnerships at BigCorp" \
  --context "co-marketing opportunity pitch" \
  --goal "explore partnership terms" \
  --channel slack \
  --tone direct \
  --timeline "2d,5d,10d"
```

## Integration with OpenClaw

The tool generates OpenClaw-compatible cron job JSON. To schedule automated reminders:

```bash
# Generate cron jobs
./tools/followup_autopilot.py \
  --person "Client" \
  --context "proposal sent" \
  --goal "get approval" \
  --timeline "1d,3d,7d" \
  --json > /tmp/followup.json

# Extract and add cron jobs (requires jq)
jq -r '.cron_jobs[] | @json' /tmp/followup.json | while read job; do
  openclaw cron add --json "$job"
done
```

Or manually copy-paste the cron job snippets from the output.

## Timeline Format

The `--timeline` argument accepts flexible formats:

- **Days:** `1d,3d,7d` → 1, 3, 7 days
- **Hours:** `12h,48h` → 0.5, 2 days
- **Mixed:** `1d,3d,1w` → 1, 3, 7 days
- **Numbers:** `1,3,7` → assumed as days

Examples:
- Quick follow-up: `12h,1d,2d`
- Standard: `1d,3d,7d`
- Persistent: `1d,3d,7d,14d,30d`
- Aggressive: `6h,1d,2d,4d`

## Best Practices

1. **Match channel to relationship:** Email for formal, DM for casual
2. **Start friendly, go direct:** Use friendly tone initially, switch to direct if no response
3. **Respect timelines:** Don't over-ping (3-4 follow-ups max)
4. **Personalize drafts:** Use generated drafts as templates, customize before sending
5. **Track responses:** Mark cron jobs complete when you get a reply

## Tips

- **A/B test tones:** Run both `--tone friendly` and `--tone direct` to compare
- **Batch generate:** Use stdin + JSON for bulk follow-up planning
- **Adjust timeline:** Shorten for hot leads (1d,2d,4d), lengthen for cold outreach (3d,7d,14d)
- **Use with CRM:** Export to JSON and integrate with your existing pipeline tools

## Limitations

- Drafts are templates — always personalize before sending
- Does not actually send messages (that's on you)
- Cron jobs require OpenClaw cron subsystem
- No response tracking (yet)

## Future Enhancements

- Response detection and auto-pause
- Multi-channel sequences (email → text → call)
- A/B testing with conversion tracking
- Integration with email/messaging APIs
- Smart timeline suggestions based on context

## Troubleshooting

**"Error: Invalid JSON input"**
→ Check stdin input is valid JSON

**Cron jobs not firing**
→ Verify OpenClaw cron subsystem is running: `openclaw cron status`

**Dates look wrong**
→ Ensure `--start` is in ISO format: `2026-02-11T09:00:00`

## License

MIT License. Use freely.

---

**Questions?** Check the examples above or run `./tools/followup_autopilot.py --help`
