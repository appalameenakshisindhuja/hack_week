# 📸 Instagram Profile Scraper & Auto-Follower Bot

This Python script uses **Selenium WebDriver** to:

✅ Log in to Instagram using a dummy account  
✅ Search and follow a target Instagram account  
✅ Extract profile information such as:
- Username
- Number of Posts
- Followers
- Following

✅ Save the scraped data to a `.txt` file

---

## 🚀 Features

- Automatically logs into Instagram with provided credentials  
- Handles cookie, save info, and notification popups  
- Navigates to a target profile  
- Extracts public data from the profile  
- Saves output to `instagram_data.txt`

---

## 📦 Requirements

- Python 3.x  
- Google Chrome  
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) installed and in PATH  
- Selenium

Install dependencies:

pip install selenium
🔐 Setup Credentials
You can either:

Set environment variables:

bash
Copy
Edit
export IG_USERNAME="your_instagram_username"
export IG_PASSWORD="your_instagram_password"
Or let the script prompt you for input.

## ⚙️ How to Run

python insta_fixed.py
The script will:

Open Instagram

Log in

Visit the target account (default: cbitosc)

Follow it

Scrape bio, followers, posts, and following

Save everything to instagram_data.txt

📝 Output Example

account_name: cbitosc

posts: 50
followers: 4,500
following: 3
🛑 Notes
Use this only with a dummy/testing account.

Instagram's HTML structure changes frequently — keep XPaths updated.

This tool does not bypass any private account restrictions.
