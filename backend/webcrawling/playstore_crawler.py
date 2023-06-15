import os
import time
import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# from webcrawling.driver_config import start_driver


def get_name_logo_url_policy_by_id(id):
    print(f'Getting data for {id}')
    name = id
    logo_url = ''
    policy = 'Error'  # has to stay because empty policy will throw an error (Todo: talk to NLP team about fixing)
    driver = None
    try:
        # Start driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=en-US')  # Set browser language to English
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=chrome_options)
        # driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        # driver = start_driver() # Todo fix import statement, so this can be used

        # Open play store for the given app package name
        url = "https://play.google.com/store/apps/details?id="
        wait = WebDriverWait(driver, 10)
        driver.get(f'{url}{id}')

        # Wait for page to load and find logo_url and app name 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[1]/img[1]')))
        logo_url_element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[1]/img[1]')
        logo_url = logo_url_element.get_attribute('src')
        name_element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span')
        name = name_element.text

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
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_policy)))
        button_policy = driver.find_element(By.XPATH, xpath_policy)
        button_policy.click()

        # Loop through until we find a new window handle and switch the driver to the new window
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # TODO check if actually html or e.g., pdf
        # Wait for next page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Check for forwarding notice
        if len(driver.find_elements(By.TAG_NAME, "title")) > 0:
            page_title = driver.find_element(By.TAG_NAME, "title")
            if page_title.get_attribute('innerHTML') == "Weiterleitungshinweis":
                link = driver.find_element(By.TAG_NAME, 'a')
                link.click()
                # Wait for next page to load
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        policy = extract_policy_from_page(driver.page_source)
        print('id:', id, 'name:', name, 'logo_url:', logo_url, '\n', policy[:100])
        return True, name, logo_url, policy

    except TimeoutException as e:
        print(e)
        print(f'Timeout occurred. The requested element {id} is either not found in the Play Store or the page experienced a timeout while loading.')
        return False, name, logo_url, policy

    except Exception as e:
        print(e)
        print(f'No app data found for {id}')
        return False, name, logo_url, policy

    finally:
        if driver is not None:
            driver.quit()


def export_policy(page, id):
    with open(f'backend/src/webcrawling/policy_export/all/{id}.txt', 'w', encoding="utf-8") as f:
        f.write(page.text)


def extract_policy_from_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    # remove header tags
    header = soup.find('header')
    if header is not None:
        header.decompose()

    # remove Navigation bar tags
    nav = soup.find('nav')
    if nav is not None:
        nav.decompose()

    # remove footer tags
    footer = soup.find('footer')
    if footer is not None:
        footer.decompose()

    # remove all tags that have classnames or ids matching the search-strings
    searchstrings = ['.*nav.*', '.*header.*', '.*footer.*']
    for searchstring in searchstrings:
        regex = re.compile(searchstring)
        for eachClass in soup.find_all("div", {"class": regex}):
            eachClass.decompose()
        for eachId in soup.find_all('div', id=regex):
            eachId.decompose()

    body = soup.find('body')
    return body.text


def handle_pdf_file(pdf_url):
    response = requests.get(pdf_url)
    # Save the downloaded PDF file to disk
    with open('downloaded.pdf', 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    id = 'com.badoo.mobile'
    get_name_logo_url_policy_by_id(id)
