
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# Configuration - replace with environment variables or prompt
USERNAME = os.getenv("IG_USERNAME") or input("Enter Instagram username: ")
PASSWORD = os.getenv("IG_PASSWORD") or input("Enter Instagram password: ")
INSTAGRAM_URL = "https://www.instagram.com/"
TARGET_ACCOUNT = "cbitosc"
OUTPUT_FILE = "instagram_data.txt"

def initialize_driver():
    options = Options()
    # Comment out next line if you want to see the browser
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def login_to_instagram(driver):
    driver.get(INSTAGRAM_URL)
    time.sleep(2)

    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only allow essential cookies')]"))
        )
        cookie_button.click()
    except Exception as e:
        print("No cookie prompt shown.")

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(5)

    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]"))
        )
        not_now_button.click()
    except:
        pass

    try:
        not_now_notifications = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
        )
        not_now_notifications.click()
    except:
        pass

def search_and_follow_account(driver, account_name):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    search_box.send_keys(account_name)
    time.sleep(2)

    first_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{account_name}/')]"))
    )
    first_result.click()
    time.sleep(3)

    try:
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Follow')]"))
        )
        follow_button.click()
        print(f"Successfully followed {account_name}")
    except:
        print(f"Could not follow {account_name} - may already be following or button not found")

def extract_account_data(driver, account_name):
    data = {}

    # Username from the URL
    data['account_name'] = account_name

    # Get bio text
    try:
        bio_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'-vDIg')]/span"))
        )
        data['bio'] = bio_element.text
    except:
        data['bio'] = "Not available"

    # Get post, followers, following
    try:
        stats = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
        )
        posts_text = stats[0].find_element(By.TAG_NAME, "span").text
        followers_text = stats[1].find_element(By.TAG_NAME, "span").get_attribute("title") or stats[1].text
        following_text = stats[2].find_element(By.TAG_NAME, "span").text

        data['posts'] = posts_text
        data['followers'] = followers_text
        data['following'] = following_text
    except Exception as e:
        data['posts'] = data['followers'] = data['following'] = "Not available"
        print("Error scraping stats:", e)

    return data


def save_data_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    print(f"Data saved to {filename}")

def main():
    driver = initialize_driver()

    try:
        login_to_instagram(driver)
        search_and_follow_account(driver, TARGET_ACCOUNT)
        account_data = extract_account_data(driver, TARGET_ACCOUNT)

        print("Extracted Account Data:")
        for key, value in account_data.items():
            print(f"{key}: {value}")

        save_data_to_file(account_data, OUTPUT_FILE)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
