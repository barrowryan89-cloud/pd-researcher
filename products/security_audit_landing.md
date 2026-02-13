# AI Agent Security Audit
## Secure Your Code Before It Ships

**Private. Discrete. Professional.**

Most AI agents run with dangerous permissions: shell access, file system write, API keys in plaintext. One vulnerability and your infrastructure — or your users' data — is compromised.

We audit agent codebases, skills, and autonomous workflows to find the flaws others miss.

---

## Why Agents Need Specialized Audits

AI agents aren't traditional software. They:
- Execute commands autonomously without human review
- Handle sensitive data through LLM context windows
- Integrate with external tools via arbitrary shell calls
- Run in loops that can amplify small bugs into large damage

Standard security scanners weren't built for this. We are.

---

## What's Found in a Typical Audit

| Risk Category | Example | Impact |
|---------------|---------|--------|
| **Command Injection** | `exec(user_input)` | Full system compromise |
| **Data Exfiltration** | API keys logged to LLM provider | Credential theft |
| **Prompt Injection** | Untrusted content in system prompt | Unauthorized actions |
| **Destructive Operations** | `rm -rf` in cleanup logic | Accidental data loss |
| **Infinite Loops** | Unbounded recursion | Resource exhaustion / cost spikes |
| **Over-Permissioning** | Broad AWS IAM scopes | Lateral movement risk |

---

## Pricing

### 🔍 Basic Scan — $250
**For: Pre-deployment sanity checks, small repos, rapid validation**

- Automated static analysis (up to 50 files)
- Detection of common red flags: `curl | bash`, unsafe evals, destructive commands
- Plain text report with high-risk lines flagged
- Pass/Fail recommendation with quick fixes
- **24-hour turnaround**

### 🔬 Deep Dive — $1,500
**For: Production agents, high-stakes deployments, compliance requirements**

- Everything in Basic Scan
- Manual line-by-line logic review by senior engineer
- Data exfiltration risk assessment
- Prompt injection vulnerability analysis
- Logic flaw detection (loops, resource exhaustion, race conditions)
- Detailed remediation guide with code examples
- 30-minute consultation call to review findings
- **3-5 business day turnaround**

---

## The Process

**1. Submit** — Share repo access or codebase archive + intended use case

**2. Audit** — We analyze permissions, tool usage, and execution paths

**3. Report** — Receive confidential findings with severity ratings and fixes

**4. Verify** — Optional consultation call to review critical issues

---

## What You Get

- **Executive Summary** — Risk level at a glance
- **Itemized Findings** — Critical, High, Medium, Low severity ratings
- **Flagged Code Snippets** — Exact locations requiring attention
- **Remediation Steps** — Specific fixes with example code
- **Confidential Delivery** — Plain text or PDF, your choice

---

## Requirements

To begin the audit, we need:

1. **Code Access** — Repository read access or zip archive
2. **Context** — Brief description of agent purpose and permissions
3. **Dependencies** — List of allowed external domains/APIs (if any)

---

## Who This Is For

- Agent developers shipping to production
- Teams building internal AI tools with system access
- Founders raising security questions from investors
- Enterprises with compliance requirements
- Anyone who runs `chmod +x` on AI-generated code

---

## FAQ

**Q: Do you fix the issues you find?**  
A: Audits are assessment-only. We provide detailed remediation guidance but don't modify your codebase.

**Q: What languages do you audit?**  
A: Python, JavaScript/TypeScript, Bash/shell scripts. Other languages by request.

**Q: Is my code kept confidential?**  
A: Absolutely. All audits are private. We don't retain code after delivery and will sign NDAs for enterprise engagements.

**Q: Can you audit packaged/compiled agents?**  
A: We need source code access. Obfuscated or compiled binaries require additional scoping.

**Q: What's the difference between Basic and Deep Dive?**  
A: Basic is automated scanning with quick human validation. Deep Dive is comprehensive manual review with consultation.

---

## Ready to Audit?

**Email:** barrowryan89@gmail.com  
**Subject:** START AUDIT [BASIC or DEEP]

Include your repository link or attach a zip, and we'll begin within 24 hours.

---

*PD — Private. Discrete. Secure.*  
*Sand Street Holdings*
