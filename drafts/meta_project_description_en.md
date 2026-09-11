---
title: "I Built a Bot That Writes Daily Content for Me — for $0.04/month"
date: 2026-09-11
market: en
type: meta
tags: [python, openai, automation, github-actions, google-trends]
---

# I Built a Bot That Writes Daily Content for Me — for $0.04/month

Every morning at 8am I get an email with a list of what people in Poland and the US are searching for right now. Each topic comes with a Twitter-ready post. Two full blog articles — one in Polish, one in English — are committed to a GitHub repo, ready to publish.

Total cost: about four cents a day. Two lines of config to add a new country. No server.

Here's how it works.

## The Problem It Solves

I used to check Google Trends manually — open the page, scan, take notes, forget. Classic repetitive task, classic automation candidate.

Trending searches are one of the most honest signals of what actually occupies people on a given day. Not algorithmically curated "for you" content — raw, mass interest.

## Architecture

The project is five Python modules and a YAML file for GitHub Actions.

**Trend fetching** — `pytrends` queries Google Trends for the top searches in each country. The subtle part: correct timezone and language in the request. For Poland that's `tz=60` (UTC+1) and `hl=pl-PL`. I had `tz=360` (Chicago) hardcoded for months. Polish trends were being fetched with a Chicago context. Small, dumb, hard to notice.

**Deduplication** — every trend is written to a JSON file with a timestamp. On the next run, anything seen in the last 24 hours is filtered out. Without this, the same topic would hit four emails in one day.

**Content generation** — two separate GPT models:
- `gpt-4.1-nano` for tweets (~200 chars) — the cheapest model in OpenAI's lineup
- `gpt-4.1-mini` for articles (~600 words) — noticeably better at longer coherent text

**Delivery** — HTML email via Gmail SMTP, and auto-committed article drafts pushed to the repo.

**Schedule** — GitHub Actions cron `0 6,12,18,22 * * *`. No server, no infra costs.

## What It Actually Costs

With the current config (2 markets, 3 trends, 4 runs/day):

- Tweets: ~24 calls × ~60 tokens ≈ $0.00014/day
- Articles: 2 calls × ~1200 tokens ≈ $0.0012/day
- Total: **under $0.04/month**

For comparison: a fraction of a cup of coffee.

## Error Handling Matters

Early version had zero error handling. `pytrends` rate-limits aggressively and returns empty DataFrames silently. OpenAI can time out. Gmail SMTP can fail.

Without proper try/except, any one of these would silently kill the whole GitHub Actions run — no log, no email, no draft. The new version handles each failure independently: a bad market is skipped and logged, a failed tweet generation returns `None` and the trend is still reported in the email, a SMTP error is caught and logged without crashing the article generation.

## Roadmap

Things on the list:

- **Trend filtering** — stop-word list to skip topics I don't care about
- **LinkedIn format** — separate, longer prompt for professional-tone posts
- **Twitter API** — direct auto-posting via tweepy
- **Keyword alerts** — instant email when a specific keyword hits trending
- **Blog platform** — eventually auto-publish via Ghost or WordPress API

## Get It

The project is open source: [github.com/pawellach/trends-monitor](https://github.com/pawellach/trends-monitor)

Fork it, add four GitHub Secrets, done. Details in the README.

---

*Time to write this post: 0 minutes. It was written by the same script it describes.*
