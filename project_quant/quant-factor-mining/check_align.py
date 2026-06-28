import pandas as pd

factors = pd.read_parquet("tmp/factors.parquet")
factor_tickers = set(col.rsplit("_", 1)[1] for col in factors.columns)
print("factor tickers:", len(factor_tickers))

close = pd.read_parquet("tmp/close.parquet")
close_tickers = set(close.columns)
print("close tickers:", len(close_tickers))

print("in factor not in close:", factor_tickers - close_tickers)
print("in close not in factor:", close_tickers - factor_tickers)
