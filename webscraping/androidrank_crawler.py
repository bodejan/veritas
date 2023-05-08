import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait


def get_applist():
    url = "https://androidrank.org"
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    # Get the current working directory
    cwd = os.getcwd()

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", cwd)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.get(f'{url}')

    download_csv = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/p[2]/a")
    download_csv.click()
    time.sleep(5)
    driver.quit()

