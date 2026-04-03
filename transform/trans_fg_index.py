import json
import pandas as pd

# Open the bronze Fear & Greed index file from the bronze folder.
with open("data/bronze/alternative/fg_index_2026-04-01T17-20-08.json", "r") as f:
    raw = json.load(f)

# Extract the API payload stored inside the "data" key into a DataFrame.
df = pd.DataFrame(raw["data"])

# Replace blank strings with missing values so incomplete rows can be detected.
REQUIRED_COLUMNS = ["timestamp", "value", "value_classification"]
df[REQUIRED_COLUMNS] = df[REQUIRED_COLUMNS].replace("", pd.NA)

# Coerce invalid timestamps and values to NaN/NaT instead of failing on bad input.
df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Trim classification text so whitespace-only values become missing.
df["value_classification"] = (df["value_classification"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

# Count rows that are missing any required field before dropping them.
missing_rows = df[REQUIRED_COLUMNS].isna().any(axis=1).sum()

# Keep only complete records for the silver output.
silver_df = df.dropna(subset=REQUIRED_COLUMNS).copy()

# Rename columns and cast cleaned data into the final schema.
silver_df["date"] = pd.to_datetime(silver_df["timestamp"], unit="s").dt.date
silver_df["alt_value"] = silver_df["value"].astype(int)
silver_df["alt_classification"] = silver_df["value_classification"].str.upper()

# Save cleaned file in the silver folder.
silver = silver_df[["date", "alt_value", "alt_classification"]]
silver.to_csv("data/silver/alt_daily_clean.csv", index=False)

# Display count of dropped rows from the data.
print(f"dropped {missing_rows} rows with missing required values.")
