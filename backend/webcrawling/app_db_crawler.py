import csv
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webcrawling.androidrank_crawler import click_next_page
from models import CATEGORIES

categories = CATEGORIES


def crawl_and_export_data():
    """
    Crawl app data for all categories, export the data to a JSON file, and refresh the database.
    """
    final_data = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(refresh_db, c) for c in categories.keys()]

        for future in as_completed(futures):
            result = future.result()
            final_data.extend(result)

    final_data = remove_duplicates(final_data)
    final_data.sort(key=lambda x: x['name'])  # Sort the final_data list alphabetically

    temp_file_path = "temp_db.json"
    with open(temp_file_path, "w") as outfile:
        json.dump(final_data, outfile)

    try:
        if os.path.exists("db.json"):
            os.remove("db.json")
        os.rename(temp_file_path, "db.json")
        print("Database refreshed successfully.")
    except Exception as e:
        print("An error occurred while refreshing the database.")
        print("Error:", str(e))
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def remove_duplicates(arr):
    """
    Remove duplicate dictionaries from the given list of dictionaries.

    Args:
        arr (list): The list of dictionaries.

    Returns:
        list: The list of dictionaries with duplicates removed.
    """
    unique_dicts = {tuple(d.items()) for d in arr}
    unique_arr = [dict(item) for item in unique_dicts]
    return unique_arr


def refresh_db(category):
    """
    Refresh the app data for the given category.

    Args:
        category (str): The category for which to refresh the app data.

    Returns:
        list: The list of app data for the category.
    """
    results = get_app_data(category, 250)
    return results


def get_app_data(category, number):
    """
    Get the app data for the given category.

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

            if driver is None:
                print(f'Crawled {len(results)} out of {number}')
                break
            else:
                elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ranklist > tbody:nth-child(1)')))

        if driver is not None:
            driver.quit()

    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        driver.quit()

    return results

