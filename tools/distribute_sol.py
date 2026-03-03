import os
import json
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Config
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={os.environ.get('HELIUS_API_KEY')}"
MAIN_WALLET_PATH = os.path.expanduser("~/.openclaw/workspace/keys/pd_researcher_solana_wallet.json")
SUB_WALLETS_DIR = os.path.expanduser("~/.openclaw/workspace/keys/airdrop_wallets")
AMOUNT_SOL = 0.1

def get_sub_wallets():
    wallets = []
    if not os.path.exists(SUB_WALLETS_DIR):
        return wallets
    for f in os.listdir(SUB_WALLETS_DIR):
        if f.endswith(".json"):
            with open(os.path.join(SUB_WALLETS_DIR, f)) as wf:
                data = json.load(wf)
                wallets.append((data['name'], Pubkey.from_string(data['public_key'])))
    return wallets

def distribute():
    if not os.environ.get('HELIUS_API_KEY'):
        print("Error: HELIUS_API_KEY not set")
        return

    client = Client(RPC_URL)
    
    # Load main keypair
    with open(MAIN_WALLET_PATH) as f:
        data = json.load(f)
        secret_hex = data['private_key']
        sender = Keypair.from_seed(bytes.fromhex(secret_hex))
    
    balance = client.get_balance(sender.pubkey()).value / 1e9
    print(f"Sender: {sender.pubkey()}")
    print(f"Balance: {balance:.4f} SOL")
    
    if balance < (AMOUNT_SOL * 4 + 0.01):
        print("⚠️ Insufficient balance for distribution (need ~0.41 SOL)")
        return

    receivers = get_sub_wallets()
    print(f"Distributing {AMOUNT_SOL} SOL to {len(receivers)} wallets...")
    
    for name, receiver in receivers:
        print(f"Sending {AMOUNT_SOL} SOL to {name} ({receiver})...")
        try:
            ix = transfer(
                TransferParams(
                    from_pubkey=sender.pubkey(),
                    to_pubkey=receiver,
                    lamports=int(AMOUNT_SOL * 1e9)
                )
            )
            # Create transaction
            recent_blockhash = client.get_latest_blockhash().value.blockhash
            tx = Transaction.new_signed_with_payer(
                [ix],
                sender.pubkey(),
                [sender],
                recent_blockhash
            )
            
            # Send
            resp = client.send_transaction(tx)
            print(f"  ✅ Success! Tx: {resp.value}")
        except Exception as e:
            print(f"  ❌ Failed: {e}")

if __name__ == "__main__":
    distribute()
