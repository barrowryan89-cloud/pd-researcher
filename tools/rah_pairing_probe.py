import requests

BASE_URLS = [
    "https://rentahuman.ai/api",
    "https://api.rentahuman.ai"
]
ENDPOINTS = [
    "pairing", "pairing/code", "pairing/get_code", "get_pairing_code",
    "auth/pairing", "agent/pairing", "code", "connect", "link"
]

def probe():
    for base in BASE_URLS:
        for end in ENDPOINTS:
            url = f"{base}/{end}"
            print(f"Trying {url}...", end=" ")
            try:
                resp = requests.post(url, timeout=3) # Try POST
                print(f"[POST: {resp.status_code}]", end=" ")
                
                resp_get = requests.get(url, timeout=3) # Try GET
                print(f"[GET: {resp_get.status_code}]")
                
                if 200 in [resp.status_code, resp_get.status_code]:
                    # Check if JSON contains 'code'
                    try:
                        data = resp.json() if resp.status_code == 200 else resp_get.json()
                        if 'code' in data or 'pairing_code' in data:
                            print(f"✅ FOUND PAIRING ENDPOINT: {url}")
                            print(data)
                            return
                    except:
                        pass
            except:
                print("Error")

if __name__ == "__main__":
    probe()
