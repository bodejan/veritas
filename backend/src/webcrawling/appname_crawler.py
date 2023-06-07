import csv
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from backend.src.webcrawling.androidrank_crawler import click_next_page

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
    # "Transportation": "?category=TRANSPORTATION",
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
    # "Game Family": "?category=GAME_FAMILY",
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


def refresh_db():
    final_data = []
    # crawl androidrank and get names, ids, and picture links
    for c in list(categories.keys())[:2]:
        results = get_app_data(c, 500)
        for result in results:
            final_data.append(result)

    # write data to json file
    with open("policy_export/app_data.json", "a") as outfile:
        json.dump(final_data, outfile)


def get_app_data(category, number):
    url = "https://androidrank.org/android-most-popular-google-play-apps"
    options = Options()
    options.headless = False
    # options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(options=options)
    results = []

    try:
        driver.get(f'{url}{categories[category]}')

        while len(results) < 500:

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
                    'image': picture_odd.get_attribute('src')
                }
                results.append(result_odd)

                result_even = {
                    'id': match_even.group(1),
                    'name': name_id_even.get_attribute('innerHTML'),
                    'image': picture_even.get_attribute('src')
                }
                results.append(result_even)

            # click next page and end driver when all apps crawled
            driver = click_next_page(driver)
            if driver == None:
                print(f'Crawled {len(results)} out of {number}')
                break
            else:
                time.sleep(4)

        # Quit driver if successful
        driver.quit()

    except Exception as e:
        print(f'Error while crawling top {number} from {category}')
        print(f'Current url: {driver.current_url}')
        driver.quit()

    return results


if __name__ == "__main__":
    refresh_db()
