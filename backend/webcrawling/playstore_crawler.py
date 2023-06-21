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
from langdetect import detect


# from webcrawling.driver_config import start_driver

# Custom exception class
class PDFFileException(Exception):
    pass

class LanguageException(Exception):
    pass

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
        # Set the Accept-Language header
        chrome_options.add_argument("--accept-language=en,*")  # Set Accept-Language to accept all English languages
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=chrome_options)
        # driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        # driver = start_driver() # Todo fix import statement, so this can be used

        # Open play store for the given app package name
        url = "https://play.google.com/store/apps/details?id="
        wait = WebDriverWait(driver, 10)
        driver.get(f'{url}{id}')

        # Wait for page to load and find logo_url and app name 
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        name, logo_url = extract_name_logo_url_from_page(driver.page_source, id)

        # Expand the developers contact section
        xpath_expand = '//*[@id="developer-contacts-heading"]/div[2]/button'
        button_expand = driver.find_element(By.XPATH, xpath_expand)
        button_expand.click()

        # Store the ID of the original window
        original_window = driver.current_window_handle

        # Check we don't have other windows open already
        assert len(driver.window_handles) == 1

        # Click the link which opens in a new window
        xpath_policy = '//*[@id="developer-contacts"]/div/div[last()]/div/a'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_policy)))
        button_policy = driver.find_element(By.XPATH, xpath_policy)
        button_policy.click()

        # Loop through until we find a new window handle and switch the driver to the new window
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Handle pdf policies
        is_pdf = driver.current_url.endswith(".pdf")
        if is_pdf: raise PDFFileException

        # Wait for next page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Check for forwarding notice
        if len(driver.find_elements(By.TAG_NAME, "title")) > 0:
            page_title = driver.find_element(By.TAG_NAME, "title")
            #print(driver.page_source)
            if page_title.get_attribute('innerHTML') == "Weiterleitungshinweis":
                print('Weiterleitungshinweis')
                link = driver.find_element(By.TAG_NAME, 'a')
                link.click()
                # Wait for next page to load
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        policy = extract_policy_from_page(driver.page_source)
        if detect_language(policy) != 'en': raise LanguageException
        print('id:', id, 'name:', name, 'logo_url:', logo_url, '\n', policy[:100])
        return True, name, logo_url, policy


    except LanguageException as e:
        # Handle the custom exception
        policy = f'The requested policy is not in English, consequently it receives a score of 0 in all categories. Please visit https://play.google.com/store/apps/details?id={id} for more information.' '\n' + policy
        print(f"The policy is not English, id: {id}")
        return False, name, logo_url, policy

    except PDFFileException as e:
        # Handle the custom exception
        policy = f'A PDFFileException occurred. Unfortunately we were unable to find the privacy policy. Please visit https://play.google.com/store/apps/details?id={id} for more information.'
        print(f"The webpage is a PDF file, id: {id}")
        return False, name, logo_url, policy

    except TimeoutException as e:
        policy = f'A timeout occurred. Unfortunately we were unable to find the privacy policy. Please visit https://play.google.com/store/apps/details?id={id} for more information.'
        print(e)
        print(f'Timeout occurred. The requested element {id} is either not found in the Play Store or the page experienced a timeout while loading.')
        return False, name, logo_url, policy

    except Exception as e:
        policy = f'An exception occurred. Unfortunately we were unable to find the privacy policy. Please visit https://play.google.com/store/apps/details?id={id} for more information.'
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


def extract_name_logo_url_from_page(page_source, id):
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the element using XPath
    element = soup.find('h1', itemprop='name')
    # Extract the name from the element
    name = slice_app_name(element.text) if element else id

    # Find the element using XPath
    element = soup.find('img', alt='Icon image', itemprop='image', class_='T75of cN0oRe fFmL2e')
    # Extract the logo URL from the 'src' attribute of the element
    logo_url = element['src'] if element and 'src' in element.attrs else ''

    return name, logo_url


def handle_pdf_file(pdf_url):
    response = requests.get(pdf_url)
    # Save the downloaded PDF file to disk
    with open('downloaded.pdf', 'wb') as file:
        file.write(response.content)


def slice_app_name(name):
    sliced_name = name
    delimiters = ['.', ',', '-', ':', '(']
    for delimiter in delimiters:
        if delimiter in name:
            sliced_name = name.split(delimiter, 1)[0].strip()
    print(name, "-->", sliced_name)
    return sliced_name


def detect_language(text):
    language = detect(text)
    return language

if __name__ == "__main__":
    id = 'com.badoo.mobile'
    get_name_logo_url_policy_by_id(id)
