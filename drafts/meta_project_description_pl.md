---
title: "Zbudowałem automat, który pisze za mnie codziennie — za 4 grosze"
date: 2026-09-11
market: pl
type: meta
tags: [python, openai, automatyzacja, github-actions, trendy]
---

# Zbudowałem automat, który pisze za mnie codziennie — za 4 grosze

Każdego ranka o 8:00 dostaję e-mail z listą tematów, o których w Polsce i Stanach mówi się najgłośniej. Przy każdym temacie gotowy post twitterowy. Do tego dwa artykuły blogowe — jeden po polsku, jeden po angielsku — zapisane w repozytorium na GitHubie, gotowe do publikacji.

Kosztuję się to cztery grosze dziennie. Dwa wiersze konfiguracji, żeby dodać nowy kraj. Zero serwera.

Opowiem jak to działa.

## Skąd pomysł

Śledziłem Google Trends ręcznie — wchodziłem na stronę, sprawdzałem, notowałem. Nudne, powtarzalne, zapominalne. Klassyczny kandydat do automatyzacji.

Do tego mam wrażenie, że jednym z najszczerszych sygnałów o tym, co naprawdę zajmuje ludzi danego dnia, są właśnie trending searches. Nie algorytmicznie dobrane „dla ciebie" — tylko surowy, masowy sygnał zainteresowania.

## Jak działa

Cały projekt to pięć modułów Pythona i plik YAML dla GitHub Actions.

**Pobieranie trendów** — biblioteka `pytrends` odpytuje Google Trends o top wyszukiwania dla danego kraju. Klucz: poprawna strefa czasowa i język żądania. Dla Polski to `tz=60` (UTC+1) i `hl=pl-PL`. Wcześniej miałem tam hardcoded `tz=360` (Chicago) — trendy polskie były pobierane z kontekstem chicagowskim. Małe, głupie, trudne do zauważenia.

**Deduplicacja** — każdy trend jest zapisywany do pliku JSON z timestampem. Przy kolejnym uruchomieniu trendy z ostatnich 24h są pomijane. Bez tego ten sam temat trafiałby do 4 maili dziennie.

**Generowanie treści** — dwa osobne modele GPT:
- `gpt-4.1-nano` na tweety (~200 znaków) — najtańszy model w ofercie OpenAI
- `gpt-4.1-mini` na artykuły (~600 słów) — nieco droższy, ale wyraźnie lepszy przy dłuższym tekście

**Dostarczanie** — HTML e-mail przez Gmail SMTP i auto-commit artykułów do repozytorium.

**Harmonogram** — GitHub Actions, cron `0 6,12,18,22 * * *`. Zero serwera, zero kosztów infrastruktury.

## Co kosztuje

Przy obecnej konfiguracji (2 rynki, 3 trendy, 4 uruchomienia dziennie):

- Tweety: ~24 wywołania × ~60 tokenów ≈ $0.00014/dzień
- Artykuły: 2 wywołania × ~1200 tokenów ≈ $0.0012/dzień
- Razem: **poniżej $0.04 miesięcznie**

Dla porównania: jedna kawa.

## Co planuję dodać

Projekt jest otwarty. Na najbliższej liście:

- **Filtrowanie trendów** — stop-word lista, żeby pomijać tematy z kategorii "celebryci" jeśli mnie nie interesują
- **Format LinkedIn** — osobny prompt, dłuższy i bardziej profesjonalny
- **Twitter API** — bezpośredni auto-posting przez tweepy
- **Alerty kluczowych słów** — natychmiastowy e-mail gdy konkretny temat trafi do trendów
- **Własny blog** — docelowo auto-publikacja przez API Ghost lub WordPress

## Kod i repozytoria

Projekt jest publiczny na GitHubie: [github.com/pawellach/trends-monitor](https://github.com/pawellach/trends-monitor)

Jeśli chcesz uruchomić u siebie: fork, cztery sekrety w GitHub Settings, gotowe. Szczegóły w README.

---

*Czas napisania tego posta: 0 minut. Napisał go ten sam skrypt, o którym opowiada.*
