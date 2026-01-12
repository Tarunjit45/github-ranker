import requests
import os
import json
from dotenv import load_dotenv

# File paths
DB_FILE = "leaderboard.json"
ENV_FILE = ".env"

# Try to load existing token
load_dotenv(ENV_FILE)
TOKEN = os.getenv("GITHUB_TOKEN")

def get_verified_user_data(token):
    """Fetches real data using the provided token."""
    headers = {"Authorization": f"token {token}"}
    print("\n🔐 Authenticating with GitHub...")
    
    # 1. Verify User Identity
    user_res = requests.get("https://api.github.com/user", headers=headers)
    
    if user_res.status_code != 200:
        print(f"❌ Error: {user_res.json().get('message', 'Invalid Token')}")
        return None
    
    u = user_res.json()
    username = u['login']
    
    # 2. Fetch Stars (Accurate count)
    stars = 0
    repos_res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
    if repos_res.status_code == 200:
        stars = sum(repo['stargazers_count'] for repo in repos_res.json())

    # 3. Calculate Score
    followers = u.get('followers', 0)
    public_repos = u.get('public_repos', 0)
    score = (stars * 100) + (followers * 50) + (public_repos * 10)

    return {
        "username": username,
        "avatar": u['avatar_url'],
        "stars": stars,
        "followers": followers,
        "repos": public_repos,
        "score": score
    }

def update_leaderboard(data):
    """Adds user to leaderboard.json and sorts it."""
    users = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: users = json.load(f)
            except: users = []

    # Remove old entry if exists and add new
    users = [u for u in users if u['username'].lower() != data['username'].lower()]
    users.append(data)
    users.sort(key=lambda x: x['score'], reverse=True)

    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)
    return users

if __name__ == "__main__":
    # CHECK IF TOKEN EXISTS
    if not TOKEN:
        print("\n" + "="*50)
        print("🚀 GITHUB WORLD RANKER: SETUP GUIDE")
        print("="*50)
        print("You need a GitHub Personal Access Token to join the leaderboard.")
        print("\nHOW TO GET YOUR TOKEN:")
        print("1. Visit: https://github.com/settings/tokens")
        print("2. Click 'Generate new token' (classic is easiest).")
        print("3. Select these scopes:")
        print("   ✅ 'read:user' (to see your profile)")
        print("   ✅ 'repo' or 'public_repo' (to count your stars)")
        print("4. Click 'Generate', copy the code, and paste it below.")
        print("-" * 50)
        
        TOKEN = input("🔑 Paste your GitHub Access Token: ").strip()
        
        if TOKEN:
            # Save to .env so they don't have to do it again
            with open(ENV_FILE, "w") as f:
                f.write(f"GITHUB_TOKEN={TOKEN}")
            print("✅ Token saved to .env")
        else:
            print("❌ No token provided. Exiting.")
            exit()

    # RUN THE PROCESS
    user_stats = get_verified_user_data(TOKEN)
    
    if user_stats:
        print(f"✅ Verified as: {user_stats['username']}")
        update_leaderboard(user_stats)
        
        print(f"\n--- YOUR GLOBAL STATS ---")
        print(f"User:  {user_stats['username']}")
        print(f"Score: {user_stats['score']} pts")
        print(f"Stars: {user_stats['stars']} | Followers: {user_stats['followers']}")
        print(f"\n🏆 Leaderboard updated! Push changes to GitHub to go live.")
    else:
        print("\n❌ Authentication failed. Please delete your .env file and try again.")