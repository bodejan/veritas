from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def start_driver(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en-US')  # Set browser language to English

    # Enable automatic acceptance of cookies
    chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})

    # Connect to a remote Selenium WebDriver
    driver = webdriver.Remote('http://chrome:4444/wd/hub', options=webdriver.ChromeOptions())
    driver.set_page_load_timeout(30)

    # driver.get(url)

    return driver
