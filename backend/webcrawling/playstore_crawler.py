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
from selenium.common.exceptions import NoSuchElementException
from langdetect import detect


# from webcrawling.driver_config import start_driver

# Custom exception class
class PDFFileException(Exception):
    pass

class LanguageException(Exception):
    pass

class NotInPlayStoreException(Exception):
    pass

class EmptyPolicyException(Exception):
    pass


def get_name_logo_url_policy_by_id(id):
    print(f'Getting data for {id}')
    name = id
    logo_url = ''
    policy = ''
    driver = None
    status = 'Success'
    try:
        # Start driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=en-US')  # Set browser language to English
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 0})
        chrome_options.add_argument("--enable-javascript")
        # Set the Accept-Language header
        chrome_options.add_argument("--accept-language=en,*")  # Set Accept-Language to accept all English languages
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=chrome_options)
        # driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(30)
        # driver = start_driver() # Todo fix import statement, so this can be used

        # Open play store for the given app package name
        url = "https://play.google.com/store/apps/details?id="
        wait = WebDriverWait(driver, 30)
        driver.get(f'{url}{id}')

        # Wait for page to load and find logo_url and app name 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
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
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(0.5) # Necessary as some content takes longer to load even after 'body' is visible

        # Check for forwarding notice
        if forwarding_notice_present(driver.page_source):
            link = driver.find_element(By.TAG_NAME, 'a')
            driver.get(link.text)
            # Wait for next page to load
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            time.sleep(0.5) # Necessary as some content takes longer to load even after 'body' is visible
        
        
        page = driver.page_source
        policy = extract_policy_from_page(page)
        if policy == '': raise EmptyPolicyException
        if detect_language(policy) != 'en': raise LanguageException
        if "We're sorry, the requested URL was not found on this server." in page: raise NotInPlayStoreException
        policy = add_playstore_link_to_policy(policy,id)
        print('id:', id, 'name:', name, 'logo_url:', logo_url, 'status:', status)
        return name, logo_url, policy, status


    except NotInPlayStoreException as e:
        # Handle the custom exception
        error_type = 'NotInPlayStoreException'
        error_description = 'The requested policy could not be found in the Google Play Store.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status

    except LanguageException as e:
        # Handle the custom exception
        error_type = 'LanguageException'
        error_description = 'The requested policy is not in English, therefore it receives a score of 0 across all categories.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status

    except PDFFileException as e:
        # Handle the custom exception
        error_type = 'PDFFileException'
        error_description = 'The requested policy is a pdf file. Unfortunately, we cannot handle pdf files.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status

    except TimeoutException as e:
        error_type = 'TimeoutException'
        error_description = 'A timeout occurred while loading the privacy policy.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status
    
    except NoSuchElementException as e:
        error_type = 'NoSuchElementException'
        error_description = 'Could not extract text from the providers website.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status
    
    except EmptyPolicyException as e:
        error_type = 'EmptyPolicyException'
        error_description = 'Could not extract text from the providers website. Website is empty.'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id,  '\n', e)
        status = error_type
        return name, logo_url, policy, status

    except Exception as e:
        error_type = 'UnknownException'
        error_description = f'A unknown exception occurred. Error log: {e}'
        policy = create_error_message(error_type, error_description, id, policy)
        print(error_type, error_description, id)
        status = error_type
        #export_policy_txt(policy, id)
        #export_policy_html(driver.page_source, id)
        return name, logo_url, policy, status

    finally:
        if driver is not None:
            driver.quit()

def add_playstore_link_to_policy(policy, id):
    policy = '<br>Visit <a href="https://play.google.com/store/apps/details?id=' + id + '">https://play.google.com/store/apps/details?id=' + id + '</a> for more information.<br><br>' + policy
    return policy

def create_error_message(error_type, error_description, id, policy):
    head = f'<br><strong>WARNING:</strong> An error occurred during the crawling process.<br>Type: {error_type}. <br><br>'
    links = 'Please visit <a href="https://play.google.com/store/apps/details?id=' + id + '">https://play.google.com/store/apps/details?id=' + id + '</a> for more information.<br><br><br>'
    error_message = head + error_description + '<br><br>    ' + links + policy
    return error_message

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


def forwarding_notice_present(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    forwarding_notice = soup.find('div', class_='aXgaGb')
    if forwarding_notice: 
        print(forwarding_notice.text)
        return True
    else:
        return False
    

if __name__ == "__main__":
    id = 'com.badoo.mobile'
    get_name_logo_url_policy_by_id(id)
