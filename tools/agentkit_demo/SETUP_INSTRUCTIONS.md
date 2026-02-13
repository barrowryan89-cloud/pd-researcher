# AgentKit Setup Instructions

## Current Status
✅ Project created: `tools/agentkit_demo`
⏳ Dependencies installing...

## Required API Keys

### 1. Coinbase Developer Platform (CDP) Keys
**You need to create these manually:**

1. Go to: https://portal.cdp.coinbase.com/
2. Create an account / Sign in
3. Create a new API key
4. Copy the **API Key ID** and **API Key Secret**

### 2. OpenAI API Key
Required for the LLM that powers the agent.

1. Go to: https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key

## Configuration Steps

Once you have the keys:

1. Open `tools/agentkit_demo/.env.local`
2. Fill in the following:
   ```
   OPENAI_API_KEY=sk-...
   CDP_API_KEY_ID=...
   CDP_API_KEY_SECRET=...
   ```
3. Rename the file:
   ```bash
   mv tools/agentkit_demo/.env.local tools/agentkit_demo/.env
   ```

## What This Agent Can Do

With AgentKit, the AI agent can:
- **Create wallets** on Base Sepolia testnet
- **Request testnet ETH** from faucet
- **Send transactions** (transfers, smart contract interactions)
- **Trade tokens** (via DEX protocols)
- **Deploy NFTs** and interact with marketplaces
- **Interact with DeFi** protocols (Compound, Morpho, etc.)

## Next Steps

After configuration:
```bash
cd tools/agentkit_demo
npm run dev
```

Then visit `http://localhost:3000` and start giving the agent commands like:
- "Fund my wallet with testnet ETH"
- "Check my balance"
- "Send 0.01 ETH to [address]"

## Matthew Berman's Recommendations
(To be added once video content is accessible)

## Network Info
- **Network:** Base Sepolia (testnet)
- **Wallet Type:** CDP Smart Wallet
- **Framework:** Langchain + Next.js + React

## Blocker
I cannot create the CDP API keys for you (requires KYC/human verification). Once you provide them, I will configure and run the agent.
