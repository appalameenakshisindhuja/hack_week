import requests
from bs4 import BeautifulSoup
import csv

# URL of GitHub trending page
url = "https://github.com/trending"

# Send a GET request to fetch the page
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.text, "html.parser")

# Find all repository listings
repos = soup.find_all("article", class_="Box-row")

# Extract top 5 repositories
top_5 = repos[:5]

# Prepare data list
repo_data = []

for repo in top_5:
    # Repository name is in the <h2> element with a link
    full_repo_name = repo.h2.a["href"].strip()  # e.g. /user/repo
    repo_name = full_repo_name.strip("/")
    repo_link = f"https://github.com{full_repo_name}"
    repo_data.append([repo_name, repo_link])

# Save to CSV
with open("trending_repos.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Repository Name", "Link"])
    writer.writerows(repo_data)

print("Top 5 trending repositories saved to trending_repos.csv")
