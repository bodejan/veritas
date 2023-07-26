"""
This module provides functions to scrape privacy policy information from the Google Play Store page of an app.

Functions:
- get_name_logo_url_policy_by_id(id: str) -> Tuple[str, str, str]
    Extracts the app name, logo URL, and privacy policy URL from the Google Play Store page of an app.
    Raises various exceptions for different scenarios.

- accept_all_cookies(driver: WebDriver) --> None
    Accept cookies if present.

- extract_policy_from_driver(driver: WebDriver) -> str
    Extract the policy text from the driver's current page.

- export_policy_txt(policy: str, id: str) -> None
    Export the policy text to a text file.

- export_policy_html(page_source: str, id: str) -> None
    Export the page source to an HTML file.

- add_playstore_link_to_policy(policy: str, id: str) -> str
    Add the Google Play Store link to the policy text.

- create_error_message(error_type: str, error_description: str, id: str, policy: str) -> str
    Create an error message with the given error type, description, app ID, and policy.

- extract_policy_from_page_bs4(page_source: str) -> str
    Extract the policy text from the page source using BeautifulSoup.

- extract_name_logo_url_from_page(page_source: str, id: str) -> Tuple[str, str]
    Extract the app name and logo URL from the page source.

- slice_app_name(name: str) -> str
    Slice the app name to remove unnecessary parts.

- detect_language(text: str) -> str
    Detect the language of the given text.

- forwarding_notice_present(page_source: str) -> bool
    Check if a forwarding notice is present on the page.

Custom Exceptions:
- PDFFileException: Exception raised when a PDF file is encountered instead of a web page.
- LanguageException: Exception raised when the language of the web page is not English.
- NotInPlayStoreException: Exception raised when the app is not found in the Google Play Store.
- EmptyPolicyException: Exception raised when the privacy policy is empty.
- AccessDeniedException: Exception raised when access to the web page is denied.
- NoPolicyException: Exception raised when no privacy policy is found on the web page.
- PageNotFoundException: Exception raised when no page is found.
"""

import time
import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from langdetect import detect

from src.models import LANGUAGE_DICT as language_dict


# Custom exception classes
class PDFFileException(Exception):
    """Exception raised when a PDF file is encountered instead of a web page."""

    pass


class LanguageException(Exception):
    """Exception raised when the language of the web page is not English."""

    pass


class NotInPlayStoreException(Exception):
    """Exception raised when the app is not found in the Google Play Store."""

    pass


class EmptyPolicyException(Exception):
    """Exception raised when the privacy policy is empty."""

    pass


class AccessDeniedException(Exception):
    """Exception raised when access to the web page is denied."""

    pass


class NoPolicyException(Exception):
    """Exception raised when no privacy policy is found on the web page."""

    pass

class PageNotFoundException(Exception):
    """Exception raised when no page is found (404)."""

    pass

def get_name_logo_url_policy_by_id(id: str, retries: int = 0) -> tuple[str, str, str, str]:
    """Get the app name, logo URL, and privacy policy text for the given app ID.

    Args:
        id (str): The app ID.
        retries (int, optional): The number of times to retry in case of timeouts or exceptions. Defaults to 0.

    Returns:
        tuple[str, str, str, str]: A tuple containing the app name, logo URL, privacy policy text, and status.

    Raises:
        AccessDeniedException: If the developer's website refuses to respond.
        NoPolicyException: If the developer does not provide a privacy policy.
        NotInPlayStoreException: If the policy is not found in the Google Play Store.
        LanguageException: If the policy is not in English.
        PDFFileException: If the policy file is a PDF.
        TimeoutException: If a timeout occurs while loading the privacy policy.
        NoSuchElementException: If text extraction from the developer's website fails.
        WebDriverException: If determining the loading status from the developer's website fails.
        EmptyPolicyException: If no text can be extracted from the developer's website.
        Exception: If an unknown exception occurs.
    """
    name = id
    logo_url = ''
    policy = ''
    driver = None
    status = 'Success'
    response_code = 200
    start_time = time.time()
    try:
        # Start driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=en-US')  # Set browser language to English
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 0})
        chrome_options.add_argument("--cookie-policy=accept-all")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-infobars")
        # Disable images
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        # Set the Accept-Language header
        chrome_options.add_argument("--accept-language=en,*")  # Set Accept-Language to accept all English languages
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=chrome_options)
        driver.set_page_load_timeout(30)

        # Open play store for the given app package name
        url = "https://play.google.com/store/apps/details?id="
        wait = WebDriverWait(driver, 10)
        driver.get(f'{url}{id}')

        # Wait for page to load and find logo_url and app name 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        if 'the requested URL was not found on this server' in driver.page_source:
            raise NotInPlayStoreException
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
        # Check if developer provides a policy, else throw exception
        if 'Privacy policy' in button_policy.text:
            link_to_privacy_policy = button_policy.get_attribute('href')
            driver.execute_script("window.open('" + link_to_privacy_policy + "', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
        else:
            raise NoPolicyException

        # Handle pdf policies
        is_pdf = driver.current_url.endswith(".pdf")
        if is_pdf:
            raise PDFFileException

        # Wait for next page to load
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(0.5)  # Necessary as some content takes longer to load even after 'body' is visible

        # Check for forwarding notice
        if forwarding_notice_present(driver.page_source):
            link = driver.find_element(By.TAG_NAME, 'a')
            driver.get(link.text)
            # Wait for next page to load
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

        # Accept all cookies
        accept_all_cookies(driver)

        # Get the current URL
        url = driver.current_url
        # Retrieve the response code using requests library
        try:
            response = requests.get(url, cookies=driver.get_cookies())
        except Exception:
            pass

        time.sleep(2 + retries)  # Necessary as some content takes longer to load even after 'body' is visible

        try:
            response_code = response.status_code
        except Exception:
            pass

        # Extract policy
        page = driver.page_source
        policy_bs4 = extract_policy_from_page_bs4(page)
        if policy_bs4:
            policy = policy_bs4
        else:
            time.sleep(1)
            policy = extract_policy_from_driver(driver)
        
        # Error handling
        language_code = detect_language(policy)
        if policy == '':
            raise EmptyPolicyException
        elif language_code != 'en':
            raise LanguageException
        elif response_code == 404:
            raise PageNotFoundException
        elif response_code == 403:
            # Catch false access denied response codes
            if 'access denied' in policy.lower():
                raise AccessDeniedException
            else:
                response_code = 200
        elif response_code != 200:
            # 406 might occur, if headers cannot be accepted, e.g., language requirements
            if response_code == 406: 
                pass
            else: 
                raise Exception
        
        policy = add_playstore_link_to_policy(policy, id)
        print(status.upper(),'id:', id, 'name:', name, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except AccessDeniedException as e:
        # Handle the custom exception
        error_type = 'AccessDeniedException'
        error_description = 'The developer\'s website refused to respond; access denied.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except NoPolicyException as e:
        # Handle the custom exception
        error_type = 'NoPolicyException.'
        error_description = 'The developer does not provide a privacy policy.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except NotInPlayStoreException as e:
        # Handle the custom exception
        error_type = 'NotInPlayStoreException'
        error_description = 'The requested policy could not be found in the Google Play Store.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except LanguageException as e:
        # Handle the custom exception
        error_type = 'LanguageException'
        error_description = f'The requested policy is not in English, therefore it receives a score of 0 across all categories.<br>Detected language: {language_dict[language_code]}.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except PDFFileException as e:
        # Handle the custom exception
        error_type = 'PDFFileException'
        error_description = 'The requested policy is a PDF file. Unfortunately, we cannot handle PDF files.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except TimeoutException as e:
        if retries < 2:
            retries += 1
            print(f'Retrying id {id}')
            return get_name_logo_url_policy_by_id(id, retries=retries)
        error_type = 'TimeoutException'
        error_description = 'A timeout occurred while loading the privacy policy.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except NoSuchElementException as e:
        error_type = 'NoSuchElementException'
        error_description = 'Could not extract text from the developer\'s website.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except WebDriverException as e:
        if retries < 2:
            retries += 1
            print(f'Retrying id {id}')
            return get_name_logo_url_policy_by_id(id, retries=retries)
        error_type = 'WebDriverException'
        error_description = 'Cannot determine loading status from the developer\'s website.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's', e)
        return name, logo_url, policy, status

    except EmptyPolicyException as e:
        if retries < 2:
            retries += 1
            print(f'Retrying id {id}')
            return get_name_logo_url_policy_by_id(id, retries=retries)
        error_type = 'EmptyPolicyException'
        error_description = 'Could not extract text from the developer\'s website. The website is empty.'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status
    
    except PageNotFoundException as e:
        error_type = 'PageNotFoundException'
        error_description = 'Could not find page (404).'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    except Exception as e:
        error_type = 'Exception'
        error_description = f'An exception occurred: ({type(e)}). Error log: {e}. Response code: {response_code}'
        policy = create_error_message(error_type, error_description, id, policy)
        status = error_type
        print(status.upper(),'id:', id, 'in:', time.time() - start_time, 's')
        return name, logo_url, policy, status

    finally:
        if driver is not None:
            driver.quit()

def accept_all_cookies(driver):
    try:
        # Find the cookie banner element
        cookie_banner = driver.find_element(By.XPATH, '//div[contains(@class, "cookie") or contains(@id, "banner") or contains(@class, "banner") or contains(@id, "banner") or contains(@class, "consent") or contains(@id, "consent") or contains(@class, "notice") or contains(@class, "policy") or contains(@class, "message") or contains(@class, "modal") or contains(@class, "popup") or contains(@id, "popup") or contains(@class, "accept") or contains(@id, "accept")]')

        # Try to find and click an "Accept" button
        accept_button = None
        try:
            accept_button = cookie_banner.find_element(By.XPATH, './/button[contains(text(), "Accept")]')
        except:
            pass
        try:
            accept_button = cookie_banner.find_element(By.XPATH, './/button[contains(text(), "Akzeptieren")]')
        except:
            pass

        if accept_button is not None:
            accept_button.click()
        else:
            # Dismiss the cookie banner by clicking outside or scrolling
            driver.execute_script("arguments[0].scrollIntoView(true);", cookie_banner)
    except Exception as e:
        pass

def extract_policy_from_driver(driver):
    """
    Extract the policy text from the driver's current page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        str: The extracted policy text.
    """
    try:
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_text = body_element.text
        return body_text
    except Exception as e:
        print(e)
        return None

def export_policy_txt(policy, id):
    """
    Export the policy text to a text file.

    Args:
        policy (str): The policy text.
        id (str): The app ID.

    Returns:
        None
    """
    with open(f'policy_{id}.txt', 'w') as file:
        file.write(policy)

def export_policy_html(page_source, id):
    """
    Export the page source to an HTML file.

    Args:
        page_source (str): The HTML source of the page.
        id (str): The app ID.

    Returns:
        None
    """
    with open(f'page_source_{id}.html', 'w') as file:
        file.write(page_source)

def add_playstore_link_to_policy(policy, id):
    """
    Add the Google Play Store link to the policy text.

    Args:
        policy (str): The policy text.
        id (str): The app ID.

    Returns:
        str: The policy text with the Play Store link.
    """
    policy = '<br>Visit <a href="https://play.google.com/store/apps/details?id=' + id + '">https://play.google.com/store/apps/details?id=' + id + '</a> for more information.<br><br>' + policy
    return policy

def create_error_message(error_type, error_description, id, policy):
    """
    Create an error message with the given error type, description, app ID, and policy.

    Args:
        error_type (str): The type of error.
        error_description (str): The description of the error.
        id (str): The app ID.
        policy (str): The policy text.

    Returns:
        str: The error message.
    """
    head = f'<br><strong>WARNING:</strong> An error occurred during the crawling process.<br>Type: {error_type}. <br><br>'
    links = 'Please visit <a href="https://play.google.com/store/apps/details?id=' + id + '">https://play.google.com/store/apps/details?id=' + id + '</a> for more information.<br><br><br>'
    if error_type == 'NotInPlayStoreException': links = ''
    error_message = head + error_description + '<br><br>    ' + links + policy
    return error_message

def extract_policy_from_page_bs4(page_source):
    """
    Extract the policy text from the page source using BeautifulSoup.

    Args:
        page_source (str): The HTML source of the page.

    Returns:
        str: The extracted policy text.
    """
    try:
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
        body_text = body.text.strip()
        if body_text == '':
            raise Exception
        return body.text
    except Exception as e:
        print(f'An error occurred while extracting policy from text via bs4: {type(e)}. Fallback to page source extractor')
        return None

def extract_name_logo_url_from_page(page_source, id):
    """
    Extract the app name and logo URL from the page source.

    Args:
        page_source (str): The HTML source of the page.
        id (str): The app ID.

    Returns:
        tuple[str, str]: A tuple containing the app name and logo URL.
    """
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

def slice_app_name(name):
    """
    Slice the app name to remove unnecessary parts.

    Args:
        name (str): The original app name.

    Returns:
        str: The sliced app name.
    """
    sliced_name = name
    delimiters = ['.', ',', '-', ':', '(']
    for delimiter in delimiters:
        if delimiter in name:
            sliced_name = name.split(delimiter, 1)[0].strip()
    return sliced_name

def detect_language(text):
    """
    Detect the language of the given text.

    Args:
        text (str): The text to analyze.

    Returns:
        str: The detected language code.
    """
    try:
        language_code = detect(text)
        return language_code
    except Exception as e:
        print(e)
        raise Exception

def forwarding_notice_present(page_source):
    """
    Check if a forwarding notice is present on the page.

    Args:
        page_source (str): The HTML source of the page.

    Returns:
        bool: True if a forwarding notice is present, False otherwise.
    """
    soup = BeautifulSoup(page_source, 'html.parser')
    forwarding_notice = soup.find('div', class_='aXgaGb')
    if forwarding_notice:
        return True
    else:
        return False
    