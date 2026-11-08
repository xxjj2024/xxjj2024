import urllib.parse
import urllib.request
import json
import os
from datetime import datetime, timezone

USERNAME = "xxjj2024"
DATA_DIR = "data"


def api_get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode())


def fetch_github_data():
    # 注：实际环境中由于 API 限流，建议在 GitHub Action 中传入 GITHUB_TOKEN
    headers = {
        "User-Agent": "JasmineOS-Terminal",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        data = api_get(f"https://api.github.com/users/{USERNAME}", headers)

        try:
            repos = api_get(
                f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner",
                headers,
            )
            data["total_stars"] = sum(repo.get("stargazers_count", 0) for repo in repos)
        except Exception as e:
            data["total_stars"] = None
            print(f"Stars unavailable: {e}")

        try:
            year = datetime.now(timezone.utc).year
            query = urllib.parse.quote(
                f"author:{USERNAME} committer-date:>={year}-01-01"
            )
            search = api_get(
                f"https://api.github.com/search/commits?q={query}&per_page=1",
                headers,
            )
            data["commits_ytd"] = search.get("total_count")
        except Exception as e:
            data["commits_ytd"] = None
            print(f"Commits unavailable: {e}")

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(f"{DATA_DIR}/github.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("Telemetry data fetched successfully.")
    except Exception as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    fetch_github_data()
