class AndroidApp:
    """
    Represents an Android app.

    Attributes:
        name (str): The name of the app.
        id (str): The ID of the app.
        logo_url (str): The URL of the app's logo.
        policy (str): The policy text of the app.
        scores (dict): The scores associated with the app's policy.
        status (str): The status of the app.
    """

    def __init__(self, name=None, id=None, logo_url=None, policy=None, scores=None, status=None):
        """
        Initializes an instance of the AndroidApp class.

        Args:
            name (str): The name of the app.
            id (str): The ID of the app.
            logo_url (str): The URL of the app's logo.
            policy (str): The policy text of the app.
            scores (dict): The scores associated with the app's policy.
            status (str): The status of the app.
        """
        self.status = status
        self.name = name
        self.id = id
        self.logo_url = logo_url
        self.policy = policy
        self.scores = scores


CATEGORIES = {
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

ZERO_SCORES = {
    'Data Recipients': 0,
    'Safeguards Copy': 0,
    'Processing Purpose': 0,
    'Data Categories': 0,
    'Source of Data': 0,
    'Right to Erase': 0,
    'Right to Restrict': 0,
    'Right to Access': 0,
    'Right to Object': 0,
    'Withdraw Consent': 0,
    'Right to Portability': 0,
    'Profiling': 0,
    'Controller Contact': 0,
    'Provision Requirement': 0,
    'Storage Period': 0,
    'Lodge Complaint': 0,
    'DPO Contact': 0,
    'Adequacy Decision': 0
}