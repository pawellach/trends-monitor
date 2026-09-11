import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
EMAIL_PASS = os.getenv('EMAIL_PASS')

MARKETS = {
    'pl': {'country': 'poland',        'lang': 'polish',  'hl': 'pl-PL', 'tz': 60},
    'us': {'country': 'united_states', 'lang': 'english', 'hl': 'en-US', 'tz': 300},
}

TRENDS_PER_MARKET = 3
TWEET_MODEL = 'gpt-4.1-nano'
ARTICLE_MODEL = 'gpt-4.1-mini'
