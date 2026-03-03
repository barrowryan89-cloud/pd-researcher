import requests
import time

CODE = "RENT-Q9C9"
URL = f"https://rentahuman.ai/api/pairing/status?code={CODE}"

def poll():
    print(f"Polling for {CODE}...")
    for _ in range(10):
        try:
            resp = requests.get(URL, timeout=5)
            print(f"[{resp.status_code}]", end=" ")
            if resp.status_code == 200:
                data = resp.json()
                if "api_key" in data:
                    print(f"\n✅ SUCCESS! Key: {data['api_key']}")
                    return
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    poll()
