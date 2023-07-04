"""
The script contains classes and functions for managing Android apps and constant values stored in dictionaries.
"""

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
"""
Dictionary mapping category keys to query parameters for androidrank.com.

This constant provides a mapping between category keys and their corresponding query parameters for the androidrank.com website.
Each key-value pair in this dictionary represents a category key and its corresponding query parameter.

The query parameter is used to filter the apps on the website based on the specified category.

"""

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
"""
Dictionary representing zero scores for all privacy categories.

This constant contains key-value pairs where the keys represent different categories
and the values represent the corresponding zero scores. These scores are associated
with a privacy policy.

The categories included in this dictionary are:
- Data Recipients
- Safeguards Copy
- Processing Purpose
- Data Categories
- Source of Data
- Right to Erase
- Right to Restrict
- Right to Access
- Right to Object
- Withdraw Consent
- Right to Portability
- Profiling
- Controller Contact
- Provision Requirement
- Storage Period
- Lodge Complaint
- DPO Contact
- Adequacy Decision

"""

LANGUAGE_DICT = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'sq': 'Albanian',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Tagalog',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)'
}
"""
Dictionary mapping language codes to language names.

This constant provides a mapping between language codes and their corresponding language names.
It is primarily used by the langdetect library for identifying the language based on the language code.

Each key-value pair in this dictionary represents a language code and its corresponding language name.

"""
