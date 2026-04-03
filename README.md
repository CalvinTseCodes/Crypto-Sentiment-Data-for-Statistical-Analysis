# Crypto-Sentiment-Data-for-Statistical-Analysis
Built a small data pipeline that pulls data from public APIs, stores raw snapshots locally, and transforms the data into a clean, joined dataset using a medallion architecture

## BTC candle transform note
`transform/trans_binance_btc_candles.py` now handles missing Binance candle values by coercing blank or invalid numeric fields to `NaN`, dropping rows that are missing any required BTC candle field (`open_time`, `open`, `high`, `low`, `close`, `volume`), and printing how many rows were removed before saving `data/silver/btc_daily_clean.csv`.

AI Disclosure
AI TOOL USED: Gemini and Codex
WHAT IT HELPED WITH: coding, debugging errors, brainstorming possible hypothesis tests
WHAT I HAD TO FIND MYSELF: When I was trying to load the request library in the terminal, it kept giving an error. Saying that virtual environment didn't match. Gemini suggestions weren't helping me. I finally went online and found a stack overflow post where someone had the same problem. I had pyproject.toml file outside of my folder that the terminal was reading from. I deleted it and I was then able to add the requests library.
