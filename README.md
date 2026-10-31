<div align="center">

# 📈 Trends Monitor

**Automated daily trend tracking with AI-powered insights — delivered to your inbox**

[![Scheduler](https://img.shields.io/github/actions/workflow/status/pawellach/trends-monitor/schedule.yml?label=scheduler&logo=github-actions&logoColor=white)](../../actions/workflows/schedule.yml)
[![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/powered%20by-GPT--4.1-412991?logo=openai&logoColor=white)](https://openai.com)

[Features](#-features) · [How It Works](#-how-it-works) · [Setup](#-setup) · [Configuration](#-configuration) · [Roadmap](#-roadmap)

</div>

---

Trends Monitor pulls the hottest Google Search trends for Poland 🇵🇱 and the United States 🇺🇸 four times a day, generates punchy Twitter-ready posts for each topic using GPT, and delivers everything neatly to your inbox.

On the **morning run** it also drafts a full blog article covering the day's top stories — saved as markdown in `drafts/` and auto-committed to the repo, ready to publish with one click.

---

## ✨ Features

| | |
|---|---|
| 🔄 **Real-time trends** | Google Trends data refreshed 4× daily (06:00, 12:00, 18:00, 22:00 UTC) |
| 🤖 **AI tweet generation** | Punchy 200-char posts per trend via gpt-4.1-nano (cheapest model) |
| 📝 **Daily article drafts** | ~600-word blog articles per market, generated every morning |
| 🔁 **Smart deduplication** | Each trend appears at most once per 24-hour window |
| 📧 **HTML email digest** | Styled summary delivered every run |
| 💾 **Auto-committed drafts** | Articles pushed to `drafts/` branch automatically |
| ⚙️ **Zero-config markets** | Add a new country in one line of `config.py` |

---

## ⚙️ How It Works

```
GitHub Actions (cron 4×/day)
        │
        ▼
 google_trends.py ──► pytrends API
        │
        ▼
 deduplicator.py  ──► data/seen_trends.json  (24h window)
        │
   ┌────┴────┐
   ▼         ▼ (morning only)
generator  article_generator
(tweets)   (blog drafts)
   │         │
   ▼         ▼
mailer.py  publisher.py
(HTML      (drafts/*.md
  email)    + git push)
```

**Morning run (06:00 UTC):** trends → tweets + full article → HTML email + committed drafts

**Standard runs (12:00, 18:00, 22:00 UTC):** trends → tweets → HTML email

---

## 🚀 Setup

### 1. Fork & clone

```bash
git clone https://github.com/your-username/trends-monitor.git
cd trends-monitor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Fill in your values
```

### 4. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | Your [OpenAI API key](https://platform.openai.com/api-keys) |
| `EMAIL_FROM` | Gmail address used to send summaries |
| `EMAIL_TO` | Address to receive summaries (can be the same) |
| `EMAIL_PASS` | Gmail [App Password](https://support.google.com/accounts/answer/185833) (not your account password) |

### 5. Enable Actions

Enable GitHub Actions in your fork — the scheduler starts on the next cron trigger. You can also trigger it manually via **Actions → Trends Monitor Scheduler → Run workflow**.

---

## 🔧 Configuration

All market and model settings live in `src/config.py`:

```python
MARKETS = {
    'pl': {'country': 'poland',        'lang': 'polish',  'hl': 'pl-PL', 'tz': 60},
    'us': {'country': 'united_states', 'lang': 'english', 'hl': 'en-US', 'tz': 300},
    # Add any market supported by pytrends — one line, done:
    # 'de': {'country': 'germany', 'lang': 'german', 'hl': 'de-DE', 'tz': 60},
}

TRENDS_PER_MARKET = 3    # how many trends to process per run per market
TWEET_MODEL       = 'gpt-4.1-nano'   # cheapest; great for short posts
ARTICLE_MODEL     = 'gpt-4.1-mini'   # better quality for longer content
```

### Running locally

```bash
# Standard run (tweets only)
python src/main.py

# Morning run (tweets + article drafts)
RUN_TYPE=morning python src/main.py
```

---

## 📤 Output

### Email digest

```
Subject: Trends Summary — 2026-09-11 06:00 UTC

── PL ──────────────────────────────────────
Sztuczna inteligencja
  AI zmienia rynek pracy — 65% firm planuje wdrożenia do końca roku.

Wybory samorządowe
  Polacy coraz chętniej szukają informacji o kandydatach online.

── US ──────────────────────────────────────
Taylor Swift
  Taylor Swift tops charts again — and the internet has thoughts. 🎶

iPhone 17
  Apple's new iPhone 17 leaks are here and they don't disappoint.
```

### Article drafts

Morning runs commit markdown files to `drafts/`:

```
drafts/
├── 2026-09-11_pl.md     ← Polish article with YAML frontmatter
└── 2026-09-11_en.md     ← English article with YAML frontmatter
```

Each draft includes title, date, source trends in the frontmatter, and ~600 words of structured content ready to copy-paste into any blogging platform.

---

## 🗺️ Roadmap

- [ ] Trend filtering — stop-word list to skip irrelevant topics
- [ ] LinkedIn post format — separate, longer-form prompt
- [ ] Weekly digest — top 10 trends of the week (Sunday 08:00 UTC)
- [ ] Twitter/X auto-post via API v2 (`tweepy`)
- [ ] Keyword alerts — instant email when a custom keyword hits trends
- [ ] Blog platform integration — Ghost / Hashnode / WordPress API
- [ ] DALL·E cover image prompt generation for articles
- [ ] RSS feed auto-generated from article drafts

---

## 📋 Requirements

- Python 3.11+
- GitHub account (for Actions)
- OpenAI API key
- Gmail account with [App Passwords](https://support.google.com/accounts/answer/185833) enabled

---

## 📄 License

MIT © [Paweł Lach](https://github.com/pawellach)

---

<details>
<summary>🇵🇱 Opis po polsku</summary>

## Trends Monitor — co to jest i jak działa

**Trends Monitor** to zautomatyzowany skrypt Python monitorujący trendy Google dla Polski i USA. Działa 4 razy dziennie przez GitHub Actions — bez serwera, bez infrastruktury, w 100% bezpłatnie (poza kosztami API OpenAI, które przy tym użyciu wynoszą kilka groszy dziennie).

### Co robi

Co 6 godzin skrypt:
1. Pobiera top trending searches z Google Trends dla każdego skonfigurowanego rynku
2. Filtruje trendy widziane w ostatnich 24h (bez powtórek)
3. Generuje krótki post twitterowy dla każdego tematu (gpt-4.1-nano)
4. Wysyła HTML e-mail z podsumowaniem

Rano (06:00 UTC, 08:00 CEST) **dodatkowo**:
- Generuje artykuł blogowy (~600 słów) po polsku i po angielsku
- Zapisuje artykuły jako markdown w katalogu `drafts/`
- Auto-commituje pliki do repozytorium

### Koszty

Przy 4 uruchomieniach dziennie, 3 trendach per market, 2 rynkach:
- Tweety: ~24 wywołania × ~50 tokenów ≈ **$0.0001/dzień** (gpt-4.1-nano)
- Artykuły: 2 wywołania × ~1000 tokenów ≈ **$0.001/dzień** (gpt-4.1-mini)
- Łącznie: **poniżej $0.04/miesiąc**

### Konfiguracja

Skopiuj `.env.example` → `.env`, uzupełnij klucze. W GitHub: dodaj 4 sekrety (`OPENAI_API_KEY`, `EMAIL_FROM`, `EMAIL_TO`, `EMAIL_PASS`). Gotowe.

Nowy rynek (np. Niemcy) to jeden wpis w słowniku `MARKETS` w `src/config.py`.

</details>
