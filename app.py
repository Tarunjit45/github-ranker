import requests
import os
import json
from dotenv import load_dotenv

# 1. Load your verified token
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}
DB_FILE = "leaderboard.json"

def get_verified_user_data():
    """Fetches data for the ACTUAL owner of the token."""
    print("🔐 Authenticating with GitHub...")
    
    # This endpoint '/user' returns the authenticated user's data ONLY
    user_res = requests.get(f"https://api.github.com/user", headers=HEADERS)
    
    if user_res.status_code != 200:
        print("❌ Auth Failed! Please check if your GITHUB_TOKEN is correct in .env")
        return None
    
    u = user_res.json()
    username = u['login']
    print(f"✅ Verified as: {username}")
    
    # Deep Scan for Stars
    stars = 0
    page = 1
    while page <= 5:
        repo_res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100&page={page}", headers=HEADERS)
        repos = repo_res.json()
        if not repos or not isinstance(repos, list): break
        stars += sum(r['stargazers_count'] for r in repos)
        page += 1

    return {
        "username": username,
        "name": u.get('name') or username,
        "avatar": u['avatar_url'],
        "stars": stars,
        "followers": u.get('followers', 0),
        "repos": u.get('public_repos', 0),
        "score": (stars * 100) + (u.get('followers', 0) * 50) + (u.get('public_repos', 0) * 10)
    }

def update_leaderboard(user_data):
    users = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            users = json.load(f)

    # Update the user if they exist, otherwise add them
    users = [u for u in users if u['username'].lower() != user_data['username'].lower()]
    users.append(user_data)
    
    # Sort by World Score
    users = sorted(users, key=lambda x: x['score'], reverse=True)

    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)
    return users

def generate_web_page(users):
    rows = ""
    for i, u in enumerate(users):
        rank = i + 1
        # Style the rows
        rows += f"""
        <tr>
            <td class="rank">#{rank}</td>
            <td><img src="{u['avatar']}" class="pfp"> <strong>{u['username']}</strong></td>
            <td>{u['stars']}</td>
            <td>{u['followers']}</td>
            <td class="score">{u['score']}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <style>
            body {{ background: #0d1117; color: #c9d1d9; font-family: sans-serif; text-align: center; }}
            .container {{ width: 80%; margin: auto; padding-top: 50px; }}
            table {{ width: 100%; border-collapse: collapse; background: #161b22; border-radius: 8px; overflow: hidden; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #30363d; text-align: left; }}
            th {{ background: #21262d; color: #58a6ff; }}
            .pfp {{ width: 35px; border-radius: 50%; vertical-align: middle; margin-right: 10px; }}
            .score {{ font-weight: bold; color: #3fb950; }}
            .rank {{ font-weight: bold; color: #f0883e; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌎 Verified World Leaderboard</h1>
            <table>
                <tr><th>Rank</th><th>User</th><th>Stars ⭐</th><th>Followers 👥</th><th>Total Score</th></tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    my_data = get_verified_user_data()
    if my_data:
        leaderboard = update_leaderboard(my_data)
        generate_web_page(leaderboard)
        print("\n--- YOUR GLOBAL STATS ---")
        print(f"Ranked as: {my_data['username']}")
        print(f"Total Score: {my_data['score']}")
        print(f"Leaderboard updated in 'index.html'!")