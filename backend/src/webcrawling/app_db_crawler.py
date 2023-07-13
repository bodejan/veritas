"""
This script contains functions to crawl app data from the AndroidRank website, export the data to a JSON file, and refresh the database.

The main functions in this script are:
- crawl_db: Refreshes the app data for all categories, exports the data to a JSON file, and refreshes the database.
- remove_duplicates: Removes duplicate dictionaries from a given list of dictionaries.
- get_app_data: Retrieves the app data for a given category.

Note: This script requires the Selenium library and a running Selenium WebDriver server.

"""

import json
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.webcrawling.androidrank_crawler import click_next_page
from src.models import CATEGORIES

categories = CATEGORIES
number_apps_per_category = 20

def crawl_db():
    """
    Refreshes the app data for all categories, exports the data to a JSON file, and refreshes the database.

    Raises:
        Exception: If less than 75% of the expected app data is crawled.
    """
    final_data = []

    for category in categories.keys():
        results = get_app_data(category, number_apps_per_category)
        print(f'Crawled {len(results)} out of {number_apps_per_category} for {category}')
        final_data.extend(results)
    print(f'CRAWL_DB_RESULT: Crawled {len(final_data)} out of {len(CATEGORIES)*number_apps_per_category}')
    # Indication that an error occurred during the crawling process 
    # Allow 25% of the crawling to fail, as db has no claim to completeness
    # E.g., due to network connectivity issues during the crawling process
    if len(final_data) < len(CATEGORIES)*number_apps_per_category*0.75:
        raise Exception
    final_data = remove_duplicates(final_data)
    # Sort the array alphabetically by the "name" key, putting numbers after "z"
    final_data.sort(key=lambda x: (x['name'][0].isdigit(), x['name'][0].isalpha(), x['name']))

    temp_file_path = "src/temp_db.json"
    with open(temp_file_path, "w") as outfile:
        json.dump(final_data, outfile, indent=4)

    try:
        if os.path.exists("src/db.json"):
            os.remove("src/db.json")
        os.rename(temp_file_path, "src/db.json")
        print("Database refreshed successfully.")
    except Exception as e:
        print("An error occurred while refreshing the database.")
        print("Error:", str(e))
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def remove_duplicates(arr):
    """
    Removes duplicate dictionaries from the given list of dictionaries.

    Args:
        arr (list): The list of dictionaries.

    Returns:
        list: The list of dictionaries with duplicates removed.
    """
    unique_dicts = {tuple(d.items()) for d in arr}
    unique_arr = [dict(item) for item in unique_dicts]
    return unique_arr


def get_app_data(category, number):
    """
    Retrieves the app data for the given category.

    Args:
        category (str): The category for which to retrieve the app data.
        number (int): The number of app data to retrieve.

    Returns:
        list: The list of app data for the category.
    """
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en-US')  # Set browser language to English
    chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})
    driver = webdriver.Remote('http://chrome:4444/wd/hub', options=chrome_options)
    driver.set_page_load_timeout(30)

    results = []

    try:
        driver.get(f'{url}{categories[category]}')

        while len(results) < number:
            for i in range(2, 22, 2):
                name_id_odd = driver.find_element(By.CSS_SELECTOR, f'tr.odd:nth-child({i}) > td:nth-child(2) > a:nth-child(1)')
                picture_odd = driver.find_element(By.CSS_SELECTOR, f'tr.odd:nth-child({i}) > td:nth-child(3) > img:nth-child(1)')
                name_id_even = driver.find_element(By.CSS_SELECTOR, f'tr.even:nth-child({i+1}) > td:nth-child(2) > a:nth-child(1)')
                picture_even = driver.find_element(By.CSS_SELECTOR, f'tr.even:nth-child({i+1}) > td:nth-child(3) > img:nth-child(1)')

                regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
                match_odd = re.search(regex, name_id_odd.get_attribute('href'))
                match_even = re.search(regex, name_id_even.get_attribute('href'))

                result_odd = {
                    'id': match_odd.group(1),
                    'name': name_id_odd.get_attribute('innerHTML'),
                    'logo_url': picture_odd.get_attribute('src')
                }
                results.append(result_odd)

                result_even = {
                    'id': match_even.group(1),
                    'name': name_id_even.get_attribute('innerHTML'),
                    'logo_url': picture_even.get_attribute('src')
                }
                results.append(result_even)

            driver = click_next_page(driver)
            time.sleep(1.5)

            if driver is None:
                print(f'Crawled {len(results)} out of {number}')
                break
            else:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ranklist > tbody:nth-child(1)')))

        if driver is not None:
            driver.quit()

    except Exception as e:
        print(f'Error while crawling top {number} from {category}', e)
        driver.quit()

    return results
