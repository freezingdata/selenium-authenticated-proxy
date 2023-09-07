import undetected_chromedriver as uc
from selenium import webdriver

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")

from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
proxy_url = input("Enter Proxy URL with auth: ")
proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)

# Enrich Chrome options with proxy authentication
chrome_options = proxy_helper.enrich_chrome_options(chrome_options)


driver = uc.Chrome(driver_executable_path="C:/Users/hmues/AppData/Roaming/SNH Titan/addins/chrome/chromedriver/snh_chromedriver.exe", browser_executable_path="C:/Users/hmues/AppData/Roaming/SNH Titan/addins/chrome/chrome/snh_chrome.exe", options=chrome_options)
driver.get("https://api.ipify.org?format=json")
import time
time.sleep(1)
print(driver.page_source)
time.sleep(100)
