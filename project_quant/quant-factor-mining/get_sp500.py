import pandas as pd
factors = pd.read_parquet("tmp/factors.parquet")

# 随便挑一只股票，对比两个因子的值
ticker = "AAPL"
print("DailyReturn:")
print(factors[f"DailyReturn_{ticker}"].head(10))
print("\nExcessReturn:")
print(factors[f"ExcessReturn_{ticker}"].head(10))
print("\n两者差异:")
print((factors[f"DailyReturn_{ticker}"] - factors[f"ExcessReturn_{ticker}"]).abs().sum())