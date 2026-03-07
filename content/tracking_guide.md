# How to Track Your Airdrop Farming Activity (And Why It Matters)

## Why Track Your Farming?

1. **Tax Compliance** — Airdrops are taxable events in most jurisdictions
2. **Eligibility Proof** — Document your activity for potential claims
3. **Performance Analysis** — See which protocols are most profitable
4. **Portfolio Management** — Know where your funds are deployed

## What to Track

### Essential Data Points
- Date of each deposit/withdrawal
- Amount and token type
- Protocol used
- Transaction hash
- USD value at time of transaction

### For Each Protocol
- Total points accumulated
- Daily/weekly activity log
- Health factor (for lending protocols)
- Yield earned (if applicable)

## Tracking Methods

### Method 1: Spreadsheet (Beginner-Friendly)
Create columns for:
- Date
- Protocol
- Action (deposit/borrow/swap)
- Amount
- Token
- Tx Hash
- Notes

### Method 2: CLI Tool (Power Users)
Use the farming tracker tool:
```bash
python3 farming_tracker.py add my_wallet ADDRESS
python3 farming_tracker.py log my_wallet marginfi deposit 0.5
```

Benefits:
- Automated logging
- JSON export for taxes
- Historical analysis

### Method 3: Custom Database (Advanced)
Build your own tracking system:
- PostgreSQL or SQLite
- Web dashboard
- Automated imports from blockchain

## Tax Implications

**Disclaimer: Not tax advice. Consult a professional.**

### Airdrop Receipt
- Usually taxable as ordinary income
- Based on fair market value at time of receipt
- Document the date and value

### Token Sale
- Capital gains/losses
- Short-term (< 1 year) vs long-term
- Track cost basis

### Yield/Interest
- Taxable as income
- Report annually

## Sample Tracking Entry

```json
{
  "date": "2025-02-27",
  "protocol": "marginfi",
  "wallet": "farm_wallet_1",
  "action": "deposit",
  "amount": 0.5,
  "token": "SOL",
  "usd_value": 75.00,
  "tx_hash": "5x...abc",
  "points_before": 1250,
  "points_after": 1300
}
```

## Recommended Tools

### Tax Software
- CoinTracker
- Koinly
- CoinLedger
- TokenTax

### Blockchain Explorers
- Solscan
- SolanaFM
- Birdeye

### Portfolio Trackers
- DeBank
- Zapper
- APY.vision

## Best Practices

1. **Log immediately** — Don't rely on memory
2. **Screenshot points** — Weekly backup
3. **Export regularly** — Don't lose data
4. **Use consistent format** — Easier analysis
5. **Back up everything** — Cloud + local

## Common Mistakes

1. **Not tracking gas fees** — Deductible expense
2. **Missing airdrop dates** — Affects tax year
3. **No cost basis** — Can't calculate gains
4. **Inconsistent logging** — Incomplete records

## Get the Tracker Tool

Free with the airdrop farming guide:

**$9** — Includes:
- CLI farming tracker
- Balance checker
- Airdrop estimator
- Complete strategy guide

**BTC:** bc1qq0eanq0cj79jrz59nswdyae2zl7f24u5lse8mj  
**SOL:** FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ

Email barrowryan89@gmail.com with tx hash.
