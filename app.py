import requests
import os
import json
from dotenv import load_dotenv

# --- CONFIGURATION ---
DB_FILE = "leaderboard.json"
ENV_FILE = ".env"

# Load existing token
load_dotenv(ENV_FILE)
TOKEN = os.getenv("GITHUB_TOKEN")

def get_verified_user_data(token):
    """Fetches real-time verified data from GitHub."""
    headers = {"Authorization": f"token {token}"}
    print("\n🔐 Authenticating with GitHub...")
    
    # Verify Identity
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        return None
    
    u = user_res.json()
    username = u['login']
    
    # Fetch Stars (Scans first 100 repos)
    repos_res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
    stars = sum(repo['stargazers_count'] for repo in repos_res.json()) if repos_res.status_code == 200 else 0
    
    # Calculate Score: Stars (100pts), Followers (50pts), Repos (10pts)
    followers = u.get('followers', 0)
    repos_count = u.get('public_repos', 0)
    score = (stars * 100) + (followers * 50) + (repos_count * 10)
    
    return {
        "username": username,
        "name": u.get('name') or username,
        "avatar": u['avatar_url'],
        "stars": stars,
        "followers": followers,
        "repos": repos_count,
        "score": score
    }

def update_leaderboard_files(data):
    """Updates JSON database and generates a professional HTML page."""
    # 1. Update JSON
    users = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: users = json.load(f)
            except: users = []
    
    # Update existing or add new
    users = [u for u in users if u['username'].lower() != data['username'].lower()]
    users.append(data)
    users.sort(key=lambda x: x['score'], reverse=True)
    
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

    # 2. Generate Professional HTML
    table_rows = ""
    for i, u in enumerate(users):
        rank = i + 1
        rank_class = "rank-1" if rank == 1 else "rank-2" if rank == 2 else "rank-3" if rank == 3 else ""
        table_rows += f"""
        <tr class="{rank_class}">
            <td>{rank}</td>
            <td class="user-cell">
                <img src="{u['avatar']}" class="avatar">
                <span>{u['username']}</span>
            </td>
            <td>{u['stars']} ⭐</td>
            <td>{u['followers']} 👥</td>
            <td class="score-cell">{u['score']}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub World Ranking</title>
        <style>
            body {{ background: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 50px; }}
            h1 {{ color: #58a6ff; font-size: 2.5rem; margin-bottom: 10px; }}
            .leaderboard-table {{ width: 100%; max-width: 900px; border-collapse: collapse; background: #161b22; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            th, td {{ padding: 15px 20px; text-align: left; border-bottom: 1px solid #30363d; }}
            th {{ background: #21262d; color: #8b949e; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; }}
            .avatar {{ width: 35px; height: 35px; border-radius: 50%; margin-right: 12px; vertical-align: middle; border: 2px solid #30363d; }}
            .user-cell {{ display: flex; align-items: center; font-weight: 600; color: #f0f6fc; }}
            .score-cell {{ font-weight: bold; color: #3fb950; font-size: 1.1rem; }}
            .rank-1 {{ background: rgba(212, 175, 55, 0.1); }}
            .rank-2 {{ background: rgba(192, 192, 192, 0.05); }}
            tr:hover {{ background: #1c2128; transition: 0.2s; }}
        </style>
    </head>
    <body>
        <h1>🏆 Global GitHub Leaderboard</h1>
        <p>Real-time ranking based on Stars, Followers, and Repos</p>
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Developer</th>
                    <th>Stars</th>
                    <th>Followers</th>
                    <th>World Score</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        <p style="margin-top: 20px; color: #8b949e;">Clone the repo to join the ranking!</p>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    return users

if __name__ == "__main__":
    if not TOKEN:
        print("\n" + "="*50)
        print("🚀 GITHUB WORLD RANKER: SETUP GUIDE")
        print("="*50)
        print("1. Visit: https://github.com/settings/tokens")
        print("2. Generate a token (classic) with 'read:user' and 'repo' scopes.")
        print("-" * 50)
        
        TOKEN = input("🔑 Paste your GitHub Access Token: ").strip()
        if TOKEN:
            with open(ENV_FILE, "w") as f:
                f.write(f"GITHUB_TOKEN={TOKEN}")
        else:
            print("❌ No token provided. Exiting."); exit()

    stats = get_verified_user_data(TOKEN)
    if stats:
        all_users = update_leaderboard_files(stats)
        my_rank = next(i for i, u in enumerate(all_users) if u['username'] == stats['username']) + 1
        
        print(f"\n✅ Verified as: {stats['username']}")
        print(f"📈 Your World Rank: #{my_rank}")
        print(f"🔥 Total Score: {stats['score']} pts")
        print(f"\n🏆 Leaderboard updated! Run 'git push' to update the website.")
    else:
        print("\n❌ Auth failed. Delete .env and try again.")