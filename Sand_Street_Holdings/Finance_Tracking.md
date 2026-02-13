# Sand Street Holdings — Financial Tracking Templates

## 1. Weekly P&L Summary Layout

| **Line Item** | **This Week** | **WTD %** | **MTD** | **Budget** | **Variance** | **Notes** |
|---------------|---------------|-----------|---------|------------|--------------|-----------|
| **REVENUE** | | | | | | |
| Product Sales | | | | | | |
| Subscription Revenue | | | | | | |
| Other Income | | | | | | |
| **Total Revenue** | | | | | | |
| **COSTS** | | | | | | |
| COGS / Production | | | | | | |
| Infrastructure (APIs, Hosting) | | | | | | |
| Token Spend (LLM/API) | | | | | | |
| Payroll / Contractors | | | | | | |
| Marketing | | | | | | |
| Other OpEx | | | | | | |
| **Total Costs** | | | | | | |
| **NET PROFIT / LOSS** | | | | | | |
| **Cash on Hand** | | | — | — | — | Ending balance |

**Legend:**
- WTD % = Week-to-Date % of monthly target
- MTD = Month-to-Date cumulative
- Variance = (Actual − Budget) / Budget

---

## 2. Daily Token Spend Log

| **Date** | **Service** | **Model / Endpoint** | **Tokens In** | **Tokens Out** | **Est. Cost ($)** | **Project / Feature** | **Notes** |
|----------|-------------|----------------------|---------------|----------------|-------------------|-----------------------|-----------|
| YYYY-MM-DD | OpenAI | gpt-4o | 12,500 | 3,200 | $0.42 | Feature X | |
| YYYY-MM-DD | Anthropic | claude-3-sonnet | 8,000 | 1,500 | $0.28 | Internal Tool | |
| YYYY-MM-DD | Custom API | embeddings | 50,000 | — | $0.05 | Search Index | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| **Daily Total** | — | — | **Σ Tokens In** | **Σ Tokens Out** | **Σ Cost** | — | — |

---

## 3. Dashboard Description

### Core Metrics & Refresh Frequency

| **Metric** | **Frequency** | **Source** | **Owner** | **Alert Threshold** |
|------------|---------------|------------|-----------|---------------------|
| Revenue (Daily) | Daily | Stripe / Payments | PD | < 80% of daily target |
| Revenue (Weekly) | Weekly (Mon AM) | P&L Sheet | Ledger | Negative variance > 15% |
| Token Spend | Daily | Token Log | Ledger | Single day > $50 |
| Token Spend | Weekly | Token Log | Ledger | Week > $200 or trending +20% |
| Burn Rate | Weekly | P&L Sheet | Ledger | < 3 months runway |
| Cash Balance | Weekly | Bank / Wallet | Ledger | < $10K |
| API Uptime / Errors | Real-time | Provider dashboards | PD | > 1% error rate |

### Dashboard Views

**Executive Snapshot (Weekly)**
- Revenue MTD vs Target (bar chart)
- Net Profit/Loss trend (4-week)
- Cash runway estimate
- Top 3 cost drivers

**Token Tracker (Daily)**
- Today's spend vs 7-day average
- Spend by service (pie chart)
- Spend by project/feature
- Anomaly alerts (spike detection)

**Growth Metrics (Weekly)**
- MRR (Monthly Recurring Revenue)
- Churn rate
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value) estimate

### Quick-Start Checklist
- [ ] Copy the P&L template into Google Sheets / Notion
- [ ] Create daily token log (Sheet or Airtable)
- [ ] Set dashboard refresh schedule (daily vs weekly)
- [ ] Assign metric owners (PD / Ledger)
- [ ] Configure alert thresholds in monitoring tools
- [ ] Weekly review cadence with Ryan & PD
