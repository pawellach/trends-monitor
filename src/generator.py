import time
from openai import OpenAI
from config import OPENAI_API_KEY, TWEET_MODEL
from logger import get_logger

log = get_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_post(topic: str, lang: str, retries: int = 3) -> str | None:
    prompt = f"Write a punchy Twitter post about '{topic}' in {lang}. Max 200 characters. No filler hashtags."
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=TWEET_MODEL,
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=80,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            log.warning(f'generate_post attempt {attempt + 1}/{retries} failed for "{topic}": {e}')
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    log.error(f'generate_post gave up after {retries} attempts for "{topic}"')
    return None
