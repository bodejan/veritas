import csv
import time
from androidrank_crawler import get_applist
from playstore_crawler import get_policy

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
    #"Transportation": "?category=TRANSPORTATION",
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
    #"Game Family": "?category=GAME_FAMILY",
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

def get_all_ids():
    id_list = []
    for c in categories.keys():
        start_time = time.time()
        id_list_category = get_applist(c, 500)
        

        # Export metrics
        end_time = time.time()
        row = []
        row.append(c)
        row.append(end_time - start_time)
        row.append(len(id_list_category))
        with open('backend/src/webcrawling/policy_export/all_ids_metrics.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Category', 'Execution Time', 'Ids'])
            writer.writerow(row)

        print(f'{c}: {len(id_list_category)}/500 in {end_time - start_time}s')

        for id in id_list_category: id_list.append(id)
        id_list = list(set(id_list))

        # Export the array to a file
        with open('backend/src/webcrawling/policy_export/all_ids.txt', 'w') as f:
            for id in id_list:
                f.write("%s\n" % id)
        
def get_all_policies():
    # Import the array from the file
    ids = []
    with open(f'backend/src/webcrawling/policy_export/all_ids.txt', 'r') as f:
        for line in f:
            ids.append(line.strip())

    # Get policy
    for i in range(1002, len(ids)):
        id = ids[i]
        start_time = time.time()
        success = get_policy(id)
        end_time = time.time()
        if success: 
            print(f'{id} crawled successfully in {end_time-start_time}')
        else: 
            print(f'Unable to crawl {id}')
        # Export metrics
        row = []
        row.append(id)
        row.append(end_time - start_time)
        row.append(success)
        with open('backend/src/webcrawling/policy_export/all_policies_metric.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Id', 'Execution Time', 'Success'])
            writer.writerow(row)

# get_all_ids()
get_all_policies()

