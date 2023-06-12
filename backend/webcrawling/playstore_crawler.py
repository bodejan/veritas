import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_name_logo_url_policy_by_id(id):
    print(f'Getting data for {id}')
    name = ''
    logo_url = ''
    policy = ''
    driver = None
    try:
        # Start driver and open play store for the given app package name
        url = "https://play.google.com/store/apps/details?id="
        #driver = webdriver.Firefox()
        driver = webdriver.Remote('http://chrome:4444/wd/hub',options=webdriver.ChromeOptions())
        driver.set_page_load_timeout(30)
        driver.get(f'{url}{id}')

        # Find the image element using XPath
        logo_url_element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[1]/img[1]')
        # Retrieve the source URL of the image
        logo_url = logo_url_element.get_attribute('src')

        # Find the name element using XPath
        name_element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span')
        name = name_element.text
        
        # seconds = 4
        # driver.implicitly_wait(seconds)

        # Expand the developers contact section
        xpath_expand = "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[1]/section/header/div/div[2]/button"
        button_expand = driver.find_element(By.XPATH, xpath_expand)
        button_expand.click()
        driver.implicitly_wait(1)

        # Store the ID of the original window
        original_window = driver.current_window_handle

        # Check we don't have other windows open already
        assert len(driver.window_handles) == 1

        # Click the link which opens in a new window
        xpath_policy = "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[1]/section/div/div/div[last()]/div/a"
        button_policy = driver.find_element(By.XPATH, xpath_policy)
        button_policy.click()

        # Loop through until we find a new window handle and switch the driver to the new window
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        time.sleep(3)
        # elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body[text() != ""]')))

        # check for forwarding notice
        if len(driver.find_elements(By.TAG_NAME, "title")) > 0:
            page_title = driver.find_element(By.TAG_NAME, "title")
            print(page_title.get_attribute('innerHTML'))
            if page_title.get_attribute('innerHTML') == "Weiterleitungshinweis":
                link = driver.find_element(By.TAG_NAME, 'a')
                link.click()
                #driver.implicitly_wait(3)
                time.sleep(3)

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Write all text in the body to file
        page = driver.find_element(By.TAG_NAME, "body")
        """ with open('webcrawling/policy_export/all_policies.txt', 'a', encoding="utf-8") as f: # TODO add webcrawling/ again
            f.write(f'{id}\n')
            f.write(page.text)
            f.write(f'\n\n--------------------------------------------------------------\n\n') """

        # export_policy(page, id)
        policy = page.text
        print('id:', id, 'name:', name, 'logo_url:', logo_url, '\n', 'first 100 chars policy:', policy[:100], '\n')
        return True, name, logo_url, policy

    except Exception as e:
        print(e)
        print(f'No app data found for {id}')
        return False
    
    finally:
        if driver is not None:
            driver.quit()


def export_policy(page, id):
    with open(f'backend/src/webcrawling/policy_export/all/{id}.txt', 'w', encoding="utf-8") as f:
        f.write(page.text)
