import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models import CATEGORIES

categories = CATEGORIES


def get_ids_for_category(category, number):
    print(f'Getting top {number} ids for {category}')
    ids = []
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    driver = None
    
    try:
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=webdriver.ChromeOptions())
        driver.get(f'{url}{categories[category]}')


        while (len(ids) < number):
            time.sleep(3)
            links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
            links = list(map(lambda x: x.get_attribute("href"), links))
            # match id of apps embedded in links and add to apps
            regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
            for l in links:
                match = re.search(regex, l)
                if (match and len(ids) < number):
                    ids.append(match.group(1))

            if len(ids) == number: break
            driver = click_next_page(driver)
            if driver == None: break
        
    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        print(f'Current url: {driver.current_url}')
        print(f'Crawled {len(ids)} out of {number}')
        print(ids)

    finally:
        if driver is not None:
            driver.quit()
    
    print(f'{len(ids)}/{number} ids crawled: {ids}', '\n')
    return ids


def get_ids_on_page(ids, driver, number):
    # get all a tags with links that hold app names from one page
    try:
        links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
        links = list(map(lambda x: x.get_attribute("href"), links))
        # match id of apps embedded in links and add to apps
        regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
        for l in links:
            match = re.search(regex, l)
            if (match and len(ids) < number):
                ids.append(match.group(1))
    except Exception as e:
        print('Error while finding ids')
        print(f'Current url: {driver.current_url}')
        print(f'Crawled {len(ids)} out of {number}')
        print(ids)
        return ids

    return ids


def click_next_page(driver):
    # does not work for some reason
    # next_btn = driver.find_element(By.XPATH, "//a[@name='Next >']")
    # neither does
    # next_btn = driver.find_element(By.XPATH, '//*[@id="content"]/small/a[1||3]')    
    try:
        # Last page starts has 'start=481' - no need to click next page
        if 'start=481' not in driver.current_url:
            # "First" and "Previous" buttons are disabled on the first page resulting in a different XPATH
            if 'start=' in driver.current_url:
                wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")))
                next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")
            else:
                # Wait until the button becomes clickable
                wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[1]")))
            
            # Get the href attribute value
            href = next_btn.get_attribute('href')

            # Open next page
            driver.get(href)

    except Exception as e:
        print(f'Cannot click "next"')
        print(f'Current url: {driver.current_url}')
        print(e)
        if driver is not None:
            driver.quit()
        return None
    return driver