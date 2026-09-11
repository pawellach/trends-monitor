import os
import subprocess
from datetime import datetime, timezone
from logger import get_logger

log = get_logger(__name__)

_DRAFTS = os.path.join(os.path.dirname(__file__), '..', 'drafts')
_REPO = os.path.join(os.path.dirname(__file__), '..')


def save_draft(article: dict) -> str | None:
    os.makedirs(_DRAFTS, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    path = os.path.join(_DRAFTS, f"{date_str}_{article['market']}.md")
    trends_yaml = ', '.join(f'"{t}"' for t in article['trends'])
    safe_title = article['title'].replace('"', "'")
    content = (
        f'---\n'
        f'title: "{safe_title}"\n'
        f'date: {date_str}\n'
        f'market: {article["market"]}\n'
        f'trends: [{trends_yaml}]\n'
        f'---\n\n'
        f'# {article["title"]}\n\n'
        f'{article["body_markdown"]}\n'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    log.info(f'Draft saved: {path}')
    return path


def git_commit_drafts() -> None:
    try:
        subprocess.run(['git', 'add', 'drafts/', 'data/'], cwd=_REPO, check=True)
        diff = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=_REPO)
        if diff.returncode != 0:
            date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
            subprocess.run(
                ['git', 'commit', '-m', f'chore: auto drafts {date_str}'],
                cwd=_REPO,
                check=True,
            )
            subprocess.run(['git', 'push'], cwd=_REPO, check=True)
            log.info('Drafts committed and pushed')
        else:
            log.info('No new drafts to commit')
    except subprocess.CalledProcessError as e:
        log.error(f'git operation failed: {e}')
