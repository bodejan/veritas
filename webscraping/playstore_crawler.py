import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from androidrank_crawler import get_applist


def get_policy(package_id):

    # Start driver and open play store for the given app package name
    url = "https://play.google.com/store/apps/details?id="
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(options=options)
    driver.get(f'{url}{package_id}')

    seconds = 5
    driver.implicitly_wait(seconds)

    # Expand the developers contact section
    xpath_expand = "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[1]/section/header/div/div[2]/button"
    button_expand = driver.find_element(By.XPATH, xpath_expand)
    button_expand.click()

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1

    # Click the link which opens in a new window
    xpath_policy = "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[1]/section/div/div/div[last()]/div/a"
    button_policy = driver.find_element(By.XPATH, xpath_policy)
    button_policy.click()

    time.sleep(10)

    # Loop through until we find a new window handle and switch the driver to the new window
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    # Print all text in the body (Todo: Change to something more useful)
    page = driver.find_element(By.TAG_NAME, "body")
    # print(page.text)
    with open('policy.txt', 'a') as f:
        f.write(page.text)
        f.write('\n#############################################################################\n')

    # Close the browser with all tabs
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()
