from pytrends.request import TrendReq
from logger import get_logger

log = get_logger(__name__)


def get_trends(country: str, hl: str = 'en-US', tz: int = 300) -> list[str]:
    try:
        pytrends = TrendReq(hl=hl, tz=tz)
        trending = pytrends.trending_searches(pn=country)
        if trending.empty:
            log.warning(f'Empty trends response for {country}')
            return []
        return trending[0].tolist()[:10]
    except Exception as e:
        log.error(f'Failed to fetch trends for {country}: {e}')
        return []
