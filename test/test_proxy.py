import json
import os
import unittest

from dotenv import load_dotenv
from selenium import webdriver

from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

load_dotenv()  
PROXY_URL = os.getenv('PROXY_URL')
PUBLIC_IP = os.getenv('PUBLIC_IP')


class TestProxy(unittest.TestCase):
    def test_proxy_connection(self):
        # test n times, as it only happens sometimes
        repeat = 5
        for i in range(repeat):
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            proxy_helper = SeleniumAuthenticatedProxy(proxy_url=PROXY_URL, disable_caching=True)
            proxy_helper.enrich_chrome_options(chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('https://httpbin.org/ip')
            import time 
            time.sleep(1000)
            json_str = driver.execute_script('return document.body.textContent')
            print(json_str)
            content = json.loads(json_str)
            self.assertEqual(content.get('origin'), PUBLIC_IP)
            driver.quit()
