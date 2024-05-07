import json
import os
import unittest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

load_dotenv()
PROXY_URL = os.getenv("PROXY_URL")
CHROME_PATH = os.getenv("CHROME_PATH")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
PUBLIC_IP = os.getenv("PUBLIC_IP")


class TestProxy(unittest.TestCase):
    def test_proxy_connection(self):

        # test n times, as it only happens sometimes
        repeat = 5
        for _ in range(repeat):
            chrome_options = webdriver.ChromeOptions()
            # https://stackoverflow.com/questions/58453327/python-selenium-chrome-extensions-with-headless-not-working
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")

            proxy_helper = SeleniumAuthenticatedProxy(
                proxy_url=PROXY_URL
            )
            proxy_helper.enrich_chrome_options(chrome_options)
            chrome_options.binary_location = CHROME_PATH
            driver = webdriver.Chrome(
                options=chrome_options,
                service=Service(CHROME_DRIVER_PATH),
            )
            driver.get("https://httpbin.org/ip")

            json_str = driver.execute_script(
                "return document.body.textContent"
            )
            content = json.loads(json_str)
            self.assertEqual(content.get("origin"), PUBLIC_IP)
            print(content.get("origin"))
            driver.quit()
