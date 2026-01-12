import requests
import os
import json
from dotenv import load_dotenv
import urllib.parse

# --- CONFIGURATION ---
DB_FILE = "leaderboard.json"
ENV_FILE = ".env"

load_dotenv(ENV_FILE)
TOKEN = os.getenv("GITHUB_TOKEN")

def get_verified_user_data(token):
    headers = {"Authorization": f"token {token}"}
    print("\n🔐 Authenticating with GitHub...")
    
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        return None
    
    u = user_res.json()
    username = u['login']
    
    repos_res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
    stars = sum(repo['stargazers_count'] for repo in repos_res.json()) if repos_res.status_code == 200 else 0
    
    followers = u.get('followers', 0)
    repos_count = u.get('public_repos', 0)
    score = (stars * 100) + (followers * 50) + (repos_count * 10)
    
    return {
        "username": username,
        "avatar": u['avatar_url'],
        "stars": stars,
        "followers": followers,
        "score": score
    }

def update_leaderboard_files(data):
    # 1. Update JSON
    users = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: users = json.load(f)
            except: users = []
    
    users = [u for u in users if u['username'].lower() != data['username'].lower()]
    users.append(data)
    users.sort(key=lambda x: x['score'], reverse=True)
    
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

    # 2. Generate HTML with Search and Share
    total_users = len(users)
    table_rows = ""
    for i, u in enumerate(users):
        rank = i + 1
        # Create Share URL
        tweet_text = f"I am ranked #{rank} on the GitHub World Leaderboard with {u['score']} points! Check your rank here: https://Tarunjit45.github.io/github-ranker/"
        share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
        
        table_rows += f"""
        <tr class="user-row">
            <td>{rank}</td>
            <td class="user-cell">
                <img src="{u['avatar']}" class="avatar">
                <span class="username">{u['username']}</span>
            </td>
            <td>{u['stars']} ⭐</td>
            <td class="score-cell">{u['score']}</td>
            <td>
                <a href="{share_url}" target="_blank" class="tweet-btn">🐦 Tweet</a>
            </td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub World Ranking</title>
        <style>
            body {{ background: #0d1117; color: #c9d1d9; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 50px; }}
            h1 {{ color: #58a6ff; margin-bottom: 5px; }}
            .stats-badge {{ background: #238636; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }}
            #searchBar {{ padding: 12px; width: 100%; max-width: 400px; border-radius: 8px; border: 1px solid #30363d; background: #161b22; color: white; margin-bottom: 20px; }}
            .leaderboard-table {{ width: 100%; max-width: 900px; border-collapse: collapse; background: #161b22; border-radius: 12px; overflow: hidden; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #30363d; }}
            th {{ background: #21262d; color: #8b949e; }}
            .avatar {{ width: 30px; border-radius: 50%; margin-right: 10px; vertical-align: middle; }}
            .score-cell {{ font-weight: bold; color: #3fb950; }}
            .tweet-btn {{ background: #1d9bf0; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.8rem; }}
            .tweet-btn:hover {{ background: #1a8cd8; }}
        </style>
    </head>
    <body>
        <h1>🏆 Global GitHub Leaderboard</h1>
        <div class="stats-badge">Total Ranked: {total_users} Developers</div>
        
        <input type="text" id="searchBar" onkeyup="searchTable()" placeholder="🔍 Search for a username...">

        <table class="leaderboard-table" id="rankTable">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Developer</th>
                    <th>Stars</th>
                    <th>World Score</th>
                    <th>Share</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <script>
        function searchTable() {{
            let input = document.getElementById("searchBar").value.toLowerCase();
            let rows = document.getElementsByClassName("user-row");
            for (let i = 0; i < rows.length; i++) {{
                let username = rows[i].getElementsByClassName("username")[0].innerText.toLowerCase();
                rows[i].style.display = username.includes(input) ? "" : "none";
            }}
        }}
        </script>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    return users

if __name__ == "__main__":
    if not TOKEN:
        print("\n🚀 GITHUB WORLD RANKER SETUP")
        TOKEN = input("🔑 Paste your GitHub Access Token: ").strip()
        if TOKEN:
            with open(ENV_FILE, "w") as f: f.write(f"GITHUB_TOKEN={TOKEN}")
        else: exit()

    stats = get_verified_user_data(TOKEN)
    if stats:
        update_leaderboard_files(stats)
        print(f"✅ Success! Run 'git push' to update the live site.")