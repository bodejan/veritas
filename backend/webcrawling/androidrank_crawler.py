import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from models import CATEGORIES

categories = CATEGORIES


def get_ids_for_category(category, number):
    apps = []
    url = "https://androidrank.org/android-most-popular-google-play-apps"

    driver = webdriver.Remote('http://chrome:4444/wd/hub',options=webdriver.ChromeOptions())



    try:
        driver.get(f'{url}{categories[category]}')

        while (len(apps) < number):
            apps = get_apps_on_page(apps, driver, number)
            if len(apps) == number: break
            driver = click_next_page(driver)
            if driver == None: 
                print(f'Crawled {len(apps)} out of {number}')
                break
            else:
                time.sleep(4)
        
        # Quit driver if successful 
        if (len(apps) == number): driver.quit()
        
    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        print(f'Current url: {driver.current_url}')
        print(f'Crawled {len(apps)} out of {number}')
        print(apps)
        driver.quit()
    print(apps)
    return apps


def get_apps_on_page(apps, driver, number):
    # get all a tags with links that hold app names from one page
    try:
        links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
        links = list(map(lambda x: x.get_attribute("href"), links))
    except Exception as e:
        print('Error while finding ids')
        print(f'Current url: {driver.current_url}')
        print(f'Crawled {len(apps)} out of {number}')
        print(apps)
        return apps
    # match id of apps embedded in links and add to apps
    regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
    for l in links:
        match = re.search(regex, l)
        if (match and len(apps) < number):
            apps.append(match.group(1))
    return apps


def click_next_page(driver):
    # does not work for some reason
    # next_btn = driver.find_element(By.XPATH, "//a[@name='Next >']")
    try:
        # Last page starts has 'start=481' - no need to click next page
        if 'start=481' not in driver.current_url:
            # "First" and "Previous" buttons are disabled on the first page resulting in a different XPATH
            if 'start=' in driver.current_url:
                next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")
            else:
                next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[1]")
            
            time.sleep(1)
            next_btn.click()
    except Exception as e:
        print(f'Cannot click "next"')
        print(f'Current url: {driver.current_url}')
        return None
    return driver
