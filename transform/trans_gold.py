import pandas as pd

#Load your two datasets
df_btc = pd.read_csv('data/silver/btc_daily_clean.csv')
df_alt = pd.read_csv('data/silver/alt_daily_clean.csv')


#Combine the 2 tables with left join on date column
#This will handle any mismatching dates. All data in fear and greed index will be joined on binance dates
combined_df = pd.merge(df_btc, df_alt, on='date', how='left')

#Dates in index that don't match binance will not be included
REQUIRED_COLUMNS = ["alt_value", "alt_classification"]
missing_rows = combined_df[REQUIRED_COLUMNS].isna().any(axis=1).sum()

#Create derived columns

#Create a column that displays daily return
combined_df['btc_daily_return'] = combined_df['btc_close'].diff().round(2)


#Create a column that displays if return is positive or not
combined_df['positive_return'] = (combined_df['btc_daily_return'] > 0).astype(int)

#Convert 'date' from string to datetime
#Create a column that identifies if the date is a weekend or not
combined_df['date'] = pd.to_datetime(combined_df['date'])
combined_df['is_weekend'] = (combined_df['date'].dt.dayofweek > 4).astype(int)

#Convert to binary for easier analysis
combined_df['is_weekend'] = combined_df['is_weekend'].astype(int)

#Save final dataset in data/gold
combined_df.to_csv("data/gold/crypto_analysis.csv", index=False)

# Display count of dropped rows from the data.
print(f"dropped {missing_rows} rows with missing required values.")