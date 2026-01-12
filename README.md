🏆 GitHub World Ranker
======================

A real-time, verified leaderboard platform that ranks developers based on their actual GitHub impact.Join the global ranking and see where you stand against the world!

🌐 Live Leaderboard
-------------------

Check out the current global standings here:👉 [**View Live Leaderboard**](https://Tarunjit45.github.io/github-ranker/)

🚀 How it Works
---------------

The **World Score** is calculated using a weighted formula that rewards high-quality contributions:

*   ⭐ **Stars:** 100 points per star
    
*   👥 **Followers:** 50 points per follower
    
*   📦 **Public Repos:** 10 points per repository
    

The tool uses **Verified Authentication**, meaning users can only add their own original accounts to the list by using their GitHub Personal Access Token.

🛠️ How to Join the Ranking
---------------------------

Follow these simple steps to get your name on the board:

### 1\. Clone the Repository

`   git clone https://github.com/Tarunjit45/github-ranker.git  cd github-ranker   `

### 2\. Install Dependencies

`   pip install requests python-dotenv   `

### 3\. Run the Verification Script

`   python app.py   `

> **Note:** The terminal will provide a step-by-step guide on how to create a GitHub Access Token.This is only used to verify your identity locally and is **never shared or uploaded**.

### 4\. Push Your Rank to the Cloud

After the script finishes updating the files locally, push them back to the repository:

`   git add leaderboard.json index.html  git commit -m "New Entry: Added my global rank"  git push origin main   `

🔒 Security
-----------

*   **Privacy:** The script only reads public profile data (Stars, Followers, Repo counts).
    
*   **Token Safety:** Your token is stored in a local .env file which is listed in .gitignore. It will never be pushed to GitHub.
    
*   **Integrity:** Only the owner of a token can add that specific account to the leaderboard.
    

🤝 Contributing
---------------

Feel free to fork this project, improve the UI, or add new features like:

*   🌍 Country Rankings
    
*   🏷️ Language-based Tiers
    

Built with ❤️ by **Tarunjit45**
