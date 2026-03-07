import os
import json
import base64
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair

RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={os.environ.get('HELIUS_API_KEY')}"
client = Client(RPC_URL)

WALLETS = [
    ("farm_wallet_1", "/home/barrowryan89/.openclaw/workspace/keys/airdrop_wallets/farm_wallet_1.json"),
    ("farm_wallet_2", "/home/barrowryan89/.openclaw/workspace/keys/airdrop_wallets/farm_wallet_2.json"),
    ("farm_wallet_3", "/home/barrowryan89/.openclaw/workspace/keys/airdrop_wallets/farm_wallet_3.json"),
    ("farm_wallet_4", "/home/barrowryan89/.openclaw/workspace/keys/airdrop_wallets/farm_wallet_4.json"),
]

def get_keypair(wallet_file):
    with open(wallet_file) as f:
        data = json.load(f)
        secret = base64.b64decode(data['private_key'])
        return Keypair.from_bytes(secret)

def execute_activity(name, wallet_file):
    try:
        print(f"\n🔄 {name}: Generating activity...")
        
        keypair = get_keypair(wallet_file)
        pubkey = keypair.pubkey()
        
        # Send 0.001 SOL to self (generates on-chain activity)
        tx = Transaction()
        tx.add(transfer(
            TransferParams(
                from_pubkey=pubkey,
                to_pubkey=pubkey,
                lamports=int(0.001 * 1e9)  # 0.001 SOL
            )
        ))
        
        recent_blockhash = client.get_latest_blockhash().value.blockhash
        tx.recent_blockhash = recent_blockhash
        
        resp = client.send_transaction(tx, keypair)
        print(f"   ✅ Success! Tx: {resp.value}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚜 SOLANA ACTIVITY GENERATION")
    print("=" * 50)
    
    if not os.environ.get('HELIUS_API_KEY'):
        print("❌ HELIUS_API_KEY not set")
        return
    
    results = []
    for name, wallet_file in WALLETS:
        if os.path.exists(wallet_file):
            success = execute_activity(name, wallet_file)
            results.append((name, success))
        else:
            print(f"❌ {name}: Wallet file not found")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 EXECUTION SUMMARY")
    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {name}: {status}")
    
    successful = sum(1 for _, s in results if s)
    print(f"\n🎯 {successful}/{len(results)} wallets active")

if __name__ == "__main__":
    main()
