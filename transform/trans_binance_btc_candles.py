import json
import pandas as pd

# Open the bronze BTC file and put it into the 'raw' variable
with open("data/bronze/binance/btc_klines_2026-04-01T15-36-32.json", "r") as f:
    raw = json.load(f)

# Extract the Binance kline payload into a DataFrame with named columns.
df = pd.DataFrame(raw,columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote","ignore"
])

# Coerce invalid or blank values to NaN first so the transform can cleanly
# detect incomplete candles instead of failing during type conversion.
REQUIRED_COLUMNS = ["open_time", "open", "high", "low", "close", "volume"]
df[REQUIRED_COLUMNS] = df[REQUIRED_COLUMNS].replace("", pd.NA)

#Turn OHLCV into numbers instead of strings. Anything that cannot be turn into numbers is changed to NA
df["open_time"] = pd.to_numeric(df["open_time"], errors="coerce")
for source_col in ["open", "high", "low", "close", "volume"]:
    df[source_col] = pd.to_numeric(df[source_col], errors="coerce")

#Count missing rows in df
missing_rows = df[REQUIRED_COLUMNS].isna().any(axis=1).sum()

#Put data into new variable drops rows that are null
silver_df = df.dropna(subset=REQUIRED_COLUMNS).copy()

# Rename columns and cast cleaned data into the final schema.
silver_df["date"] = pd.to_datetime(silver_df["open_time"], unit="ms").dt.date
silver_df["btc_open"] = silver_df["open"]
silver_df["btc_high"] = silver_df["high"]
silver_df["btc_low"] = silver_df["low"]
silver_df["btc_close"] = silver_df["close"]
silver_df["btc_volume"] = silver_df["volume"]

# Save the cleaned file in the silver folder.
silver = silver_df[["date", "btc_open", "btc_high", "btc_low", "btc_close", "btc_volume"]]
silver.to_csv("data/silver/btc_daily_clean.csv", index=False)

#Display count of dropped rows from the data
print(f"dropped {missing_rows} rows with missing required values.")
