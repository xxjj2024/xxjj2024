import urllib.request
import json
import os

USERNAME = "xxjj2024"
DATA_DIR = "data"

def fetch_github_data():
    # 注：实际环境中由于 API 限流，建议在 GitHub Action 中传入 GITHUB_TOKEN
    url = f"https://api.github.com/users/{USERNAME}"
    headers = {'User-Agent': 'JasmineOS-Terminal'}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(f"{DATA_DIR}/github.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("Telemetry data fetched successfully.")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_github_data()
