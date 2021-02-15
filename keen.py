import sys, os
import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from twilio.rest import Client


class Keen:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.to_number = os.environ["TWILIO_TO_NUMBER"]

    def eye(self, link, element_name="add-to-cart"):
        self.browser.get(link)
        try:
            notify = not self._check_if_found_before(link)
            add_to_cart_element = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, element_name))
            )
            if notify and add_to_cart_element.is_displayed():
                self._mark_link_found(link)
                message = f"Link: {link}\n Available for purchase"
                self.notify(self.to_number, message)
                print(f"Found: {link}\n")
            self.cleanup()
        except TimeoutException:
            self.cleanup()
            pass

    def _check_if_found_before(self, link):
        try:
            with open(".found") as f:
                for line in f.readlines():
                    if line.strip() == link:
                        return True
        except FileNotFoundError:
            Path(".found").touch()

        return False

    def _mark_link_found(self, link):
        with open(".found", "w+") as f:
            f.writelines([f"{link}\n"])

    def __enter__(self):
        return Keen()

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def cleanup(self):
        self.browser.quit()

    def notify(self, to_number, message):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        from_number = os.environ["TWILIO_FROM_NUMBER"]

        client = Client(account_sid, auth_token)
        message = client.messages.create(body=message, from_=from_number, to=to_number)
