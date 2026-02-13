---
name: crypto-toolbox
description: Setup + integration notes for crypto data and agent wallet tooling (Allium, Dune, Mobula, Privy, BankrBot, Solana dev skill).
metadata:
  {
    "openclaw": {
      "emoji": "🪙",
      "requires": {"notes": ["credentials for external APIs required for live calls"]}
    }
  }
---

Crypto Toolbox

Purpose
- Centralize “setups” for crypto tooling you listed.
- This is a coordination skill: it tells you what keys you need, what to install, and how to test.

Included targets
- Allium AgentHub: https://agents.allium.so/
- Dune Analytics docs: https://dune.com/docs
- Mobula: https://mobula.io/
- Privy agentic wallets: https://docs.privy.io/recipes/wallets/agentic-wallets
- BankrBot OpenClaw skills: https://github.com/BankrBot/openclaw-skills
- Solana Dev Skill: https://github.com/solana-foundation/solana-dev-skill

How to use
1) Tell PD which tool you want to activate (Allium/Dune/Mobula/Privy/Bankr/Solana).
2) Provide required credentials if needed.
3) PD produces:
- plain text setup steps
- minimal test command
- safe defaults

Security note
- Never paste private keys into chat.
- Prefer storing credentials in env vars on the VM.
- Run Audit Lite on any third-party skill repo before installing.
