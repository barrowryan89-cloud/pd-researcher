import requests
import json

URL = "https://rentahuman.ai/mcp"

def probe_rpc():
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "PD-Agent", "version": "1.0"}
        },
        "id": 1
    }
    
    print(f"Sending JSON-RPC to {URL}...")
    try:
        resp = requests.post(URL, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Content Type: {resp.headers.get('Content-Type')}")
        print(f"Body: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe_rpc()
