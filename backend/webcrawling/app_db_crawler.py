import csv
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

from .androidrank_crawler import click_next_page
from models import CATEGORIES

categories = CATEGORIES


def refresh_db():
    final_data = []
    # crawl androidrank and get names, ids, and picture links
    for c in list(categories.keys()):
        # print(c)
        results = get_app_data(c, 500)
        for result in results:
            final_data.append(result)
        print(c)

    # write data to json file
    with open("policy_export/app_data.json", "w") as outfile:
        json.dump(final_data, outfile)


def get_app_data(category, number):
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    #driver = webdriver.Firefox(options=options)
    driver = webdriver.Remote('http://chrome:4444/wd/hub',options=webdriver.ChromeOptions())
    driver.set_page_load_timeout(30)
    results = []

    try:
        driver.get(f'{url}{categories[category]}')

        while len(results) < number:

            for i in range(2, 22, 2):
                # crawl androidrank and get id, name and picture_src
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

            # click next page and end driver when all apps crawled
            # print(driver.current_url)
            driver = click_next_page(driver)

            if driver == None:
                print(f'Crawled {len(results)} out of {number}')
                break
            else:
                # time.sleep(2)
                elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ranklist > tbody:nth-child(1)')))

        # Quit driver if successful
        if driver != None:
            driver.quit()

    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        driver.quit()

    return results


if __name__ == "__main__":
    refresh_db()
