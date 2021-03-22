"""
Cookie web scraper for Maddy - Woohoo
"""
from flask import Flask
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from twilio.rest import Client
import os

app = Flask(__name__)


@app.route('/')
def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options,
    )
    driver.get("https://crumblcookies.com/")
    weekList = driver.find_element_by_id("weekly-cookie-flavors")
    weeklies = weekList.find_elements_by_tag_name("li")

    cookies = "This week's Crumbl flavors are:\n"
    for cookie in weeklies:
        flavor = cookie.find_elements_by_tag_name("h3")[0].text
        cookies += flavor + "\n"

    driver.close()

    account_id = os.environ.get("TWIL_ACCT")
    auth_token = os.environ.get("AUTH_TOKEN")
    client = Client(account_id, auth_token)

    message = client.messages.create(
        body=cookies, from_="+15036766473", to="+19524262052"
    )

    return cookies


if __name__ == "__main__":
    app.run()
