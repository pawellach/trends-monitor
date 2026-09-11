import os
from datetime import datetime, timezone
from config import MARKETS, TRENDS_PER_MARKET
from google_trends import get_trends
from generator import generate_post
from article_generator import generate_article
from deduplicator import filter_new, record
from mailer import send_email
from publisher import save_draft, git_commit_drafts
from logger import get_logger

log = get_logger(__name__)


def _is_morning_run() -> bool:
    run_type = os.getenv('RUN_TYPE', 'auto')
    if run_type == 'morning':
        return True
    if run_type == 'standard':
        return False
    return datetime.now(timezone.utc).hour == 6


def _build_html(sections: list[dict]) -> str:
    parts = ['<html><body style="font-family:sans-serif;max-width:600px;margin:auto">']
    for s in sections:
        parts.append(f'<h2 style="color:#1a1a2e;border-bottom:2px solid #eee">{s["market"].upper()}</h2>')
        for item in s['items']:
            parts.append(
                f'<div style="margin-bottom:16px">'
                f'<b style="color:#444">{item["trend"]}</b><br>'
                f'<span style="color:#666">{item["tweet"]}</span>'
                f'</div>'
            )
    parts.append('</body></html>')
    return ''.join(parts)


def run() -> None:
    morning = _is_morning_run()
    log.info(f'Run started ({"morning" if morning else "standard"})')

    email_sections = []
    article_paths = []

    for code, cfg in MARKETS.items():
        raw = get_trends(cfg['country'], hl=cfg['hl'], tz=cfg['tz'])
        if not raw:
            log.warning(f'No trends for {code}, skipping')
            continue

        fresh = filter_new(raw, code)
        if not fresh:
            log.info(f'All trends for {code} already seen in last 24h')
            continue

        working = fresh[:TRENDS_PER_MARKET]
        record(working, code)

        items = []
        for trend in working:
            tweet = generate_post(trend, cfg['lang'])
            if tweet:
                items.append({'trend': trend, 'tweet': tweet})

        if items:
            email_sections.append({'market': code, 'items': items})

        if morning:
            article = generate_article(working, cfg['lang'], code)
            if article:
                path = save_draft(article)
                if path:
                    article_paths.append(path)

    if email_sections:
        send_email(_build_html(email_sections))
    else:
        log.warning('Nothing to send — email skipped')

    if article_paths:
        git_commit_drafts()

    log.info(f'Run complete — {len(email_sections)} market(s), {len(article_paths)} article(s)')


if __name__ == '__main__':
    run()
