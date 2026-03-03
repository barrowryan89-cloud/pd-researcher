import requests
import os

API_KEY = os.environ.get("RENTAHUMAN_API_KEY", "rah_c5142d36bd2ed624b034edb05dad94e3")
BASE_URLS = [
    "https://rentahuman.ai/api",
    "https://api.rentahuman.ai",
    "https://rentahuman.ai/api/v1",
    "https://api.rentahuman.ai/v1"
]
ENDPOINTS = ["tasks", "jobs", "bounties", "orders", "requests", "human_requests"]

def probe():
    print(f"🔑 Using Key: {API_KEY[:10]}...")
    
    for base in BASE_URLS:
        for end in ENDPOINTS:
            url = f"{base}/{end}"
            print(f"Trying {url}...", end=" ")
            try:
                resp = requests.post(
                    url, 
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={"title": "Test Probe", "budget": 1},
                    timeout=5
                )
                print(f"[{resp.status_code}]")
                if resp.status_code in [200, 201]:
                    print(f"✅ SUCCESS! Endpoint found: {url}")
                    return
                elif resp.status_code == 401:
                    print("❌ Auth Failed (Key might be wrong)")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    probe()
