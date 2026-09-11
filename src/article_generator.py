import time
from openai import OpenAI
from config import OPENAI_API_KEY, ARTICLE_MODEL
from logger import get_logger

log = get_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

_PROMPTS = {
    'polish': (
        "Napisz artykuł blogowy (~600 słów) po polsku o dzisiejszych trendach: {trends}.\n\n"
        "Struktura:\n"
        "1. Chwytliwy tytuł (uwzględnij 1-2 trendy)\n"
        "2. Lead (2-3 zdania): co dziś jest na topie i dlaczego to ważne\n"
        "3. Osobna sekcja (##) dla każdego trendu: kontekst, dlaczego teraz, co to oznacza\n"
        "4. Krótkie outro z CTA (śledź, skomentuj)\n\n"
        "Zwróć wyłącznie markdown. Pierwsza linia to sam tytuł (bez #)."
    ),
    'english': (
        "Write a blog article (~600 words) in English about today's trending topics: {trends}.\n\n"
        "Structure:\n"
        "1. Catchy title (include 1-2 trends)\n"
        "2. Lead (2-3 sentences): what's trending and why it matters\n"
        "3. A dedicated ## section for each trend: context, why now, what it means\n"
        "4. Short outro with CTA (follow, comment)\n\n"
        "Return markdown only. First line is the title without #."
    ),
}


def generate_article(trends: list[str], lang: str, market_code: str, retries: int = 3) -> dict | None:
    prompt_template = _PROMPTS.get(lang, _PROMPTS['english'])
    prompt = prompt_template.format(trends=', '.join(trends))

    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=ARTICLE_MODEL,
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=1400,
            )
            content = r.choices[0].message.content.strip()
            lines = content.splitlines()
            title = lines[0].lstrip('#').strip()
            body = '\n'.join(lines[1:]).strip()
            log.info(f'Article generated for {market_code}: "{title}"')
            return {'title': title, 'body_markdown': body, 'market': market_code, 'trends': trends}
        except Exception as e:
            log.warning(f'generate_article attempt {attempt + 1}/{retries} failed for {market_code}: {e}')
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    log.error(f'generate_article gave up after {retries} attempts for {market_code}')
    return None
