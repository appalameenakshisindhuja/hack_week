# 🔥 GitHub Trending Scraper

This Python script scrapes the [GitHub Trending page](https://github.com/trending) to extract the **top 5 trending repositories** along with their names and links, and saves the results to a CSV file.

---

## 📌 Features

- Scrapes the top 5 trending repositories from GitHub.
- Extracts:
  - Repository name (e.g., `username/repository`)
  - Direct repository link (e.g., `https://github.com/username/repository`)
- Saves the data to a `trending_repos.csv` file.

---

## 📂 Output

A sample `trending_repos.csv`:

| Repository Name | Link                              |
|-----------------|-----------------------------------|
| user1/repo1     | https://github.com/user1/repo1    |
| user2/repo2     | https://github.com/user2/repo2    |

---

## 🛠️ Requirements

Make sure you have Python installed (3.6+ recommended).

Install dependencies using pip:
pip install requests beautifulsoup4

## 🚀 How to Run
Clone this repository or copy the script into a .py file.

Run the script:
python trending.py

Check the trending_repos.csv file generated in the same directory.

## 🧠 How It Works
Sends a GET request to https://github.com/trending

Parses the HTML content using BeautifulSoup

Extracts the top 5 repository entries

Writes them into a CSV file
