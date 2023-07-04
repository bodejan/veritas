import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models import CATEGORIES

categories = CATEGORIES


def get_ids_for_category(category, number):
    """
    Get the top app IDs for a given category.

    Args:
        category (str): The category for which to retrieve app IDs.
        number (int): The number of app IDs to retrieve.

    Returns:
        list: The list of app IDs.

    """
    print(f'Getting top {number} IDs for {category}')
    ids = []
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    driver = None
    
    try:
        # Start driver and open androidrank
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=en-US')  # Set browser language to English
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})
        driver = webdriver.Remote('http://chrome:4444/wd/hub', options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(f'{url}{categories[category]}')

        # Get IDs from androidrank
        while len(ids) < number:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'tbody')))
            links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
            links = list(map(lambda x: x.get_attribute("href"), links))
            # Match IDs of apps embedded in links and add to IDs
            regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
            for l in links:
                match = re.search(regex, l)
                if match and len(ids) < number:
                    ids.append(match.group(1))

            if len(ids) == number:
                break
            driver = click_next_page(driver)
            if driver is None:
                break
        
    except Exception as e:
        print(e)
        print(f'Error while crawling top {number} from {category}')
        print(f'Crawled {len(ids)} out of {number}')
        print(ids)

    finally:
        if driver is not None:
            driver.quit()
    
    print(f'{len(ids)}/{number} IDs crawled: {ids}', '\n')
    return ids


def get_ids_on_page(ids, driver, number):
    """
    Get the app IDs on the current page.

    Args:
        ids (list): The existing list of app IDs.
        driver (webdriver): The WebDriver instance.
        number (int): The max number of app IDs to retrieve.

    Returns:
        list: The updated list of app IDs.

    """
    # Get all 'a' tags with links that hold app names from one page
    try:
        links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
        links = list(map(lambda x: x.get_attribute("href"), links))
        # Match IDs of apps embedded in links and add to IDs
        regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
        for l in links:
            match = re.search(regex, l)
            if match and len(ids) < number:
                ids.append(match.group(1))
    except Exception as e:
        print('Error while finding IDs')
        print(f'Current URL: {driver.current_url}')
        print(f'Crawled {len(ids)} out of {number}')
        print(ids)
        if driver is not None:
            driver.quit()
        return ids

    return ids


def click_next_page(driver):
    """
    Click the "Next" button to navigate to the next page.

    Args:
        driver (webdriver): The WebDriver instance.

    Returns:
        webdriver or None: The updated WebDriver instance if successful, None otherwise.

    """
    try:
        # Last page starts has 'start=481' - no need to click next page
        if 'start=481' not in driver.current_url:
            # "First" and "Previous" buttons are disabled on the first page resulting in a different XPATH
            if 'start=' in driver.current_url:
                wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
                wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")))
                next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")
            else:
                # Wait until the button becomes clickable
                wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
                wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[1]")))
                next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[1]")
            
            # Get the href attribute value
            href = next_btn.get_attribute('href')

            # Open next page
            driver.get(href)
            time.sleep(1)

    except Exception as e:
        print(e)
        print(f'Cannot click "next"')
        print(f'Current URL: {driver.current_url}')
        print(f'Trying to click: {href}')

        if driver is not None:
            driver.quit()
        return None
    return driver
