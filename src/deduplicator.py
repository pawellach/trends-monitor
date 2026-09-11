import json
import os
from datetime import datetime, timezone, timedelta
from logger import get_logger

log = get_logger(__name__)

_CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'seen_trends.json')


def _load() -> list[dict]:
    try:
        with open(_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(entries: list[dict]) -> None:
    os.makedirs(os.path.dirname(_CACHE), exist_ok=True)
    with open(_CACHE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def filter_new(trends: list[str], market: str, window_hours: int = 24) -> list[str]:
    cache = _load()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    seen = {
        e['trend']
        for e in cache
        if e['market'] == market and datetime.fromisoformat(e['ts']) > cutoff
    }
    return [t for t in trends if t not in seen]


def record(trends: list[str], market: str) -> None:
    cache = _load()
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    cache = [e for e in cache if datetime.fromisoformat(e['ts']) > cutoff]
    now = datetime.now(timezone.utc).isoformat()
    cache.extend({'trend': t, 'market': market, 'ts': now} for t in trends)
    _save(cache)
    log.info(f'Recorded {len(trends)} trend(s) for {market}')
