# Recall Loop - Memory-First Workflow System

## Overview

Recall Loop is a comprehensive workflow methodology that implements persistent memory and automated follow-up for AI assistants. It ensures continuous context across sessions and automatic check-ins on important tasks.

## Purpose

This skill provides a structured approach to:
- Maintain long-term memory across sessions
- Search existing context before taking action
- Generate automated summaries and reviews
- Create intelligent follow-up reminders
- Build a searchable knowledge base over time

## Core Components

### 1. Memory Structure

```
workspace/
├── memory/
│   ├── YYYY-MM-DD.md      # Daily activity logs
│   └── archive/           # Historical logs (>30 days)
├── MEMORY.md              # Curated long-term memory
└── projects/              # Active project documentation
```

### 2. Memory-First Workflow

**Before responding to any substantive request:**

1. Search `memory/YYYY-MM-DD.md` (today + yesterday)
2. Search `MEMORY.md` for relevant context
3. Check `projects/` for related work
4. Identify relevant follow-ups
5. Respond with full context

### 3. Automated Cycles

- **Daily Summary** (evening): Compile day's activities
- **Weekly Review** (Sunday): Reflect on week's patterns
- **Project Check-Ins** (every 3 days): Surface stalled work
- **Follow-Up Reminders** (daily): Check for due items
- **Memory Maintenance** (bi-weekly): Update MEMORY.md

## Implementation

### Setup

1. Create memory folder structure:
```bash
mkdir -p memory/archive projects
touch MEMORY.md
```

2. Install cron jobs for automated workflows:
```bash
# Reference: recall_loop_cron_jobs.json
# Configure schedules based on timezone and preferences
```

3. Configure assistant to auto-load memory at session start

### Daily Log Format

```markdown
# YYYY-MM-DD

## Conversations
- [HH:MM] Topic - Key points, decisions made

## Tasks
- [ ] Incomplete task
- [x] Completed task

## Follow-Ups
- FOLLOW-UP: YYYY-MM-DD - Action item with context

## Notes
- Insights, observations, learnings
```

### Memory Search Pattern

```
Step 1: Check recent logs
- Read memory/{today}.md
- Read memory/{yesterday}.md

Step 2: Search for keywords
- grep -r "keyword" memory/
- Check MEMORY.md for related context

Step 3: Check project status
- List files in projects/ matching topic
- Read relevant project files

Step 4: Synthesize context
- Combine findings into coherent context
- Reference specific decisions or previous discussions
```

## Cron Job Examples

### Daily Evening Brief
```
Schedule: 0 22 * * *
Action: Generate summary of today's log, append to file
Deliver: Primary channel if action required
```

### Active Projects Check
```
Schedule: 0 10 */3 * *
Action: Review projects/ for stale or blocked items
Deliver: Only if attention needed
```

### Follow-Up Reminder
```
Schedule: 0 9 * * *
Action: Parse FOLLOW-UP tags, list items due today
Deliver: Morning reminder with action items
```

## Best Practices

### Writing Logs

✅ **DO:**
- Log decisions, not conversations
- Be specific: "Decided on $99/mo pricing starting March 1"
- Tag follow-ups consistently: "FOLLOW-UP: 2026-02-20 - Check invoice sent"
- Capture context for future reference

❌ **DON'T:**
- Write verbatim transcripts
- Log trivial details
- Skip days (breaks the loop)
- Forget to review your summaries

### Memory Maintenance

**Weekly:**
- Archive logs >30 days old
- Update MEMORY.md with key insights from past week
- Remove completed follow-ups

**Monthly:**
- Reorganize MEMORY.md structure
- Archive completed projects
- Review and refine cron job schedules

### Search Efficiency

- Use consistent terminology in logs
- Tag key topics: `#project-name`, `#client-name`
- Cross-reference related entries
- Maintain index in MEMORY.md for major topics

## Measuring Success

Recall Loop is working when:

✅ Assistant recalls context from weeks/months ago  
✅ No important tasks are forgotten  
✅ Follow-ups happen automatically without manual tracking  
✅ You can answer "What happened on [date]?" instantly  
✅ Projects don't stall silently  

## Troubleshooting

**Problem:** Assistant not searching memory before responding  
**Solution:** Add explicit prompt: "Check memory/ for context before answering"

**Problem:** Daily logs getting too verbose  
**Solution:** Focus on decisions and actions, not play-by-play

**Problem:** Too many cron reminders  
**Solution:** Adjust schedules, add filters for "only if action needed"

**Problem:** MEMORY.md becoming unwieldy  
**Solution:** Break into sections, archive outdated info

## Integration Points

### Works With:
- **Cron system** - For scheduled summaries and reminders
- **Search/grep** - For context lookup
- **File system** - Memory storage and project tracking
- **Messaging** - Delivery of summaries and alerts

### Requires:
- File read/write access
- Ability to schedule recurring tasks
- Basic text search capabilities

## Evolution

Recall Loop is designed to evolve with your workflow:

**Stage 1 (Week 1):** Basic logging and daily summaries  
**Stage 2 (Month 1):** Add project check-ins and follow-ups  
**Stage 3 (Month 2+):** Refine memory structure, optimize cron schedules  
**Stage 4 (Ongoing):** Customize for your specific patterns and needs  

Start simple. Add complexity only when you feel the need.

## Resources

- **Setup Guide:** products/recall_loop_template.txt
- **Cron Examples:** products/recall_loop_cron_jobs.json
- **Product Info:** products/recall_loop_offer.txt

## Version

**Version:** 1.0  
**Last Updated:** February 2026  
**Maintained By:** PD  

---

*Recall Loop: Because memory is too important to leave to chance.*
