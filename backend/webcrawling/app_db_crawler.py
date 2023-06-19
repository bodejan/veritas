import csv
import json
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from concurrent.futures import ThreadPoolExecutor, as_completed

from webcrawling.driver_config import start_driver
from webcrawling.androidrank_crawler import click_next_page
from models import CATEGORIES

categories = CATEGORIES


def crawl_and_export_data():
    final_data = []
    unique_ids = set()  # Set to store unique IDs
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(refresh_db, c) for c in categories.keys()]

        for future in as_completed(futures):
            result = future.result()
            final_data.extend(result)

        # Check for duplicates and append unique results to final_data
        for app in result:
            app_id = app['id']
            if app_id not in unique_ids:
                final_data.append(app)
                unique_ids.add(app_id)  

    # write data to a temporary file
    temp_file_path = "temp_db.json"
    with open(temp_file_path, "w") as outfile:
        json.dump(final_data, outfile)

    print(len(final_data))
    
    # replace the existing file with the new data only if successful
    try:
        # delete the existing "db.json" file if it exists
        if os.path.exists("db.json"):
            os.remove("db.json")

        # rename the temporary file to "db.json"
        os.rename(temp_file_path, "db.json")

        print("Database refreshed successfully.")
    except Exception as e:
        print("An error occurred while refreshing the database.")
        print("Error:", str(e))
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def refresh_db(category):
    results = get_app_data(category, 250)
    #print(category)
    return results


def get_app_data(category, number):
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    # Start driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en-US')  # Set browser language to English
    chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})
    driver = webdriver.Remote('http://chrome:4444/wd/hub', options=chrome_options)
    driver.set_page_load_timeout(30)
    # driver = start_driver() # Todo fix import statement, so this can be used

    results = []

    try:
        driver.get(f'{url}{categories[category]}')

        while len(results) < number:

            for i in range(2, 22, 2):
                # crawl androidrank and get id, name, and picture_src
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

            # click next page and end driver when all apps are crawled
            # print(driver.current_url)
            driver = click_next_page(driver)

            if driver is None:
                print(f'Crawled {len(results)} out of {number}')
                break
            else:
                # time.sleep(2)
                elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ranklist > tbody:nth-child(1)')))

        # Quit driver if successful
        if driver is not None:
            driver.quit()

    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        driver.quit()

    return results


#if __name__ == "__main__":
    #crawl_and_export_data()
