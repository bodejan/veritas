import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# androidrank category names and keys
# androidrank currently has issues with the categories: "Transportation" and "Game Family" 
# both links lead to "All" through no fault of the webcrawler
categories = {
    "All": "",
    "Paid": "?price=paid",
    "Free": "?price=free",
    "Art And Design": "?category=ART_AND_DESIGN",
    "Auto And Vehicles": "?category=AUTO_AND_VEHICLES",
    "Beauty": "?category=BEAUTY",
    "Books And Reference": "?category=BOOKS_AND_REFERENCE",
    "Business": "?category=BUSINESS",
    "Comics": "?category=COMICS",
    "Communication": "?category=COMMUNICATION",
    "Dating": "?category=DATING",
    "Education": "?category=EDUCATION",
    "Entertainment": "?category=ENTERTAINMENT",
    "Events": "?category=EVENTS",
    "Finance": "?category=FINANCE",
    "Food And Drink": "?category=FOOD_AND_DRINK",
    "Health And Fitness": "?category=HEALTH_AND_FITNESS",
    "House And Home": "?category=HOUSE_AND_HOME",
    "Libraries And Demo": "?category=LIBRARIES_AND_DEMO",
    "Lifestyle": "?category=LIFESTYLE",
    "Maps And Navigation": "?category=MAPS_AND_NAVIGATION",
    "Medical": "?category=MEDICAL",
    "Music And Audio": "?category=MUSIC_AND_AUDIO",
    "News And Magazines": "?category=NEWS_AND_MAGAZINES",
    "Parenting": "?category=PARENTING",
    "Personalization": "?category=PERSONALIZATION",
    "Photography": "?category=PHOTOGRAPHY",
    "Productivity": "?category=PRODUCTIVITY",
    "Shopping": "?category=SHOPPING",
    "Social": "?category=SOCIAL",
    "Sports": "?category=SPORTS",
    "Tools": "?category=TOOLS",
    "Transportation": "?category=TRANSPORTATION",
    "Travel And Local": "?category=TRAVEL_AND_LOCAL",
    "Video Players": "?category=VIDEO_PLAYERS",
    "Weather": "?category=WEATHER",
    "Game Action": "?category=GAME_ACTION",
    "Game Adventure": "?category=GAME_ADVENTURE",
    "Game Arcade": "?category=GAME_ARCADE",
    "Game Board": "?category=GAME_BOARD",
    "Game Card": "?category=GAME_CARD",
    "Game Casino": "?category=GAME_CASINO",
    "Game Casual": "?category=GAME_CASUAL",
    "Game Educational": "?category=GAME_EDUCATIONAL",
    "Game Family": "?category=GAME_FAMILY",
    "Game Music": "?category=GAME_MUSIC",
    "Game Puzzle": "?category=GAME_PUZZLE",
    "Game Racing": "?category=GAME_RACING",
    "Game Role Playing": "?category=GAME_ROLE_PLAYING",
    "Game Simulation": "?category=GAME_SIMULATION",
    "Game Sports": "?category=GAME_SPORTS",
    "Game Strategy": "?category=GAME_STRATEGY",
    "Game Trivia": "?category=GAME_TRIVIA",
    "Game Word": "?category=GAME_WORD"
}


def get_applist(category, number):
    applist = []
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    options = Options()
    options.headless = True
    # options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    driver = webdriver.Firefox(options=options)
    # print(f'{url}{categories[category]}')
    driver.get(f'{url}{categories[category]}')

    while (len(applist) < number):
        applist = get_apps_on_page(applist, driver, number)
        driver = click_next_page(driver)

    time.sleep(2)
    driver.quit()
    return applist


def get_apps_on_page(applist, driver, number):
    # get all a tags with links that hold app names from one page
    links = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
    links = list(map(lambda x: x.get_attribute("href"), links))
    # match id of apps embedded in links and add to applist
    regex = r'^https://androidrank\.org/application/.+/([^/]+)$'
    for l in links:
        match = re.search(regex, l)
        if (match and len(applist) < number):
            applist.append(match.group(1))
    return applist


def click_next_page(driver):
    # does not work for some reason
    # next_btn = driver.find_element(By.XPATH, "//a[@name='Next >']")

    # "First" and "Previous" buttons are disabled on the first page resulting in a different XPATH
    if 'start=' in driver.current_url:
        next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[3]")
    else:
        next_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/small/a[1]")
    time.sleep(2)
    next_btn.click()
    return driver
