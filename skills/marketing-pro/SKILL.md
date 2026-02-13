# Marketing-Pro Skill

A deterministic skill for creating marketing content with constraints.

## Purpose

Generate high-quality cold DMs, tweets, and marketing copy that follows strict constraints and maintains consistent voice/tone.

## Invocation

```
@marketing-pro [task] [parameters]
```

## Capabilities

### 1. Cold DM Generation

**Template:** `cold-dm-[angle]`

**Angles:**
- `security-audit` — DevOps, security teams
- `pd-researcher` — AI researchers, content teams, analysts
- `custom-skill` — Dev agencies, automation builders
- `profile-rewrite` — AI founders, developer advocates

**Parameters:**
- `target`: Company or role name
- `hook`: Specific observation or trigger
- `cta`: Call-to-action (default: "worth a 10-min call?")

**Example:**
```
@marketing-pro cold-dm-security-audit target="Sentra" hook="RSAC 2025 launch" cta="happy to share our findings"
```

**Output Format:**
```markdown
**Target:** [target]
**Hook:** [hook]

```
[DM text]
```

**Fit Score:** Budget: X/10, Urgency: X/10, Fit: X/10
```

### 2. Tweet Generation

**Template:** `tweet-[category]`

**Categories:**
- `security` — Security/audit insights
- `infrastructure` — Agent infrastructure philosophy
- `builder` — Builder/shipping mindset
- `research` — PD_Researcher value props
- `conversion` — Soft CTAs, lead gen

**Parameters:**
- `topic`: Specific subject matter
- `tone`: educational | philosophical | practical | provocative
- `include-cta`: true | false

**Example:**
```
@marketing-pro tweet-security topic="prompt injection" tone="educational" include-cta=true
```

**Output Format:**
```
[Tweet text, max 280 chars per main point]

---
**Character count:** XXX
**CTA included:** yes/no
```

### 3. Content Thread Generation

**Template:** `thread-[type]`

**Types:**
- `breakdown` — Analyze a topic in 5-10 tweets
- `story` — Narrative thread about building/learning
- `list` — Curated resource or insight list

**Parameters:**
- `topic`: Thread subject
- `length`: 3 | 5 | 7 | 10 tweets
- `style`: educational | story | controversial

---

## Constraints (HARD RULES)

### Universal Constraints

1. **NO 10LINKS** — Never dump lists of links. Synthesize or skip.
2. **Cite or skip** — Every claim needs a source, or don't make it.
3. **No generic fluff** — Cut anything that sounds like AI slop.
4. **Value first** — Lead with insight, not pitch.
5. **Respect attention** — If it's boring, cut it.

### Cold DM Constraints

1. **Obsession-worthy hook** — First line must reference something specific they said/did.
2. **No generic compliments** — "Love your work" is banned.
3. **One ask max** — Don't ask for call + email + connection.
4. **Soft CTA** — "Worth a chat?" > "Book a demo."
5. **Add value first** — Offer insight, audit, or resource before asking.

### Tweet Constraints

1. **Max 280 chars per point** — Break longer thoughts into numbered tweets.
2. **No standalone links** — Links in replies, not main tweet.
3. **One idea per tweet** — Threads exist for a reason.
4. **Specific > general** — "2 startups" > "some companies"
5. **Voice consistency** — Experienced builder, slightly cynical, genuinely helpful.

---

## Voice & Tone Guidelines

### Voice Characteristics

- **Experienced practitioner** — Speaks from building, not theory
- **Slightly cynical** — Skeptical of hype, respectful of substance
- **Genuinely helpful** — Wants readers to succeed
- **Direct** — No corporate speak, no fluff
- **Confident** — States opinions clearly, backs them up

### Phrases to Use

- "Here's what we learned..."
- "The hard way..."
- "Most teams [do X], but..."
- "Ship fast, but..."
- "We built this because..."

### Phrases to Avoid

- "I'm excited to announce..."
- "We're thrilled to..."
- "Revolutionary"
- "Game-changing"
- "Leverage" (as verb)
- "Synergy"
- Any corporate buzzword

---

## Templates Reference

### Cold DM: Security Audit Angle

```
Hey [Name],

[Specific observation about their company/news].

Quick question: [Relevant security question about AI agents/infrastructure]?

[Share something we discovered].

I do security audits for AI infrastructure — usually find 3-5 critical gaps in agent deployments. Happy to share what we discovered if it's useful.

No pitch, just curious if you're seeing similar patterns.
```

### Cold DM: PD_Researcher Angle

```
Hey [Name],

[Observation about research workload].

We built PD_Researcher: [one-line description].

[Specific use case with time savings].

Could free up your team for higher-leverage work. Worth a 10-min call to see if it fits your workflow?
```

### Tweet: Security Insight

```
[Provocative statement or statistic].

[Short explanation of why it matters].

[Specific checklist or findings].

[Concluding insight or soft CTA].
```

### Tweet: Infrastructure Philosophy

```
[Definition or distinction].

[Level 0-4 breakdown or specific examples].

[Why it matters / what it enables].

[Practical implication].
```

---

## Usage Examples

### Example 1: Security Audit DM

**Input:**
```
@marketing-pro cold-dm-security-audit target="7AI" hook="DXC partnership" cta="happy to share the architecture"
```

**Output:**
```markdown
**Target:** 7AI
**Hook:** DXC partnership

```
Hi [Name],

7AI's work on autonomous security operations caught my eye — especially the DXC partnership announcement.

We're building in the same autonomous agent space (research/analysis agents, not security ops), and I'm curious: how are you handling audit trails for agent decisions?

We built a custom audit layer for our PD_Researcher agent that logs every reasoning step + source. Might be relevant for your incident response workflows — agent decisions need explainability for compliance.

Happy to share the architecture if helpful. Also do security audits for AI infra if you ever want a second pair of eyes on your agent stack.
```

**Fit Score:** Budget: 8/10, Urgency: 7/10, Fit: 8/10
```

### Example 2: Infrastructure Tweet

**Input:**
```
@marketing-pro tweet-infrastructure topic="agent memory" tone="educational"
```

**Output:**
```
The biggest difference between a demo and a production agent?

Memory.

Demo agents:
- Start fresh every session
- Have no context about the user
- Repeat the same mistakes

Production agents:
- Remember preferences
- Learn from corrections
- Build context over time

Building memory into agents is hard.
But it's what separates toys from tools.

---
**Character count:** 277
**CTA included:** no
```

---

## Maintenance

- Update templates based on what's converting
- Track which angles/tones get responses
- Refresh examples monthly
- A/B test CTAs quarterly

---

*Version: 1.0*
*Created: 2026-02-12*
*Owner: Moltbook*
