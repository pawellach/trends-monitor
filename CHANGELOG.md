# Changelog

## [0.1.0] — 2026-10-31

### Added
- Google Trends fetching for Poland and USA via pytrends (4×/day via GitHub Actions)
- GPT-4.1-nano tweet generation per trend (~200 chars)
- GPT-4.1-mini article generation on morning run (~600 words, PL + EN)
- Smart 24h deduplication (seen_trends.json)
- HTML email digest via Gmail SMTP
- Auto-committed article drafts pushed to `drafts/`
- Zero-config market extension via `src/config.py`
- `.env.example` with all required secrets documented
