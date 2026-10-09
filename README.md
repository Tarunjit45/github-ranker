# 🏆 GitHub Ranker — Real-Time Developer Impact Leaderboard

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub API](https://img.shields.io/badge/API-GitHub%20REST%20v3-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/rest)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**GitHub Ranker** is a real-time developer leaderboard engine that calculates and ranks engineers based on verifiable open-source impact across GitHub.

---

## 📌 Scoring Methodology

Unlike superficial metrics that only count vanity metrics or automated bot commits, GitHub Ranker balances multiple dimensions:

```
+--------------------------------------------------------------+
|                     GitHub REST API v3                       |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                   Ingestion & Verification                   |
|       Total Stars Earned | Public Repositories | PRs         |
|         Followers Count  | Verified Commits    | Issues      |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                 Weighted Composite Scoring                   |
| Score = (Stars * 10) + (Followers * 5) + (Repos * 2) + Commits|
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                 Cached Store: leaderboard.json               |
|            Rendered via responsive `index.html`              |
+--------------------------------------------------------------+
```

---

## 📁 Repository Structure

```text
github-ranker/
├── app.py              # Ingestion engine, GitHub API aggregator & ranking calculator
├── index.html          # Clean, responsive leaderboard web dashboard
├── leaderboard.json    # Cached ranking database and verified player profiles
├── LICENSE             # MIT License
└── README.md
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository:

```bash
git clone https://github.com/Tarunjit45/github-ranker.git
cd github-ranker

pip install requests python-dotenv
```

### 2. Configure GitHub Token
Set up your personal access token in `.env` to prevent rate limits:

```env
GITHUB_TOKEN=ghp_your_github_token_here
```

### 3. Run Ranking Update
```bash
python app.py
```

### 4. View Leaderboard
Open `index.html` in your browser to view the real-time ranked roster.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
