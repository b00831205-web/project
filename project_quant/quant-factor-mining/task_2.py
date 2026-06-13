import pandas as pd
import os

if "__name__"=="__main__":
    df = pd.DataFrame(pd.read_parquet("/tmp/raw_data.parquet"))
    df = df.ffill(inplace = True)
    df.to_parquet("/tmp/proceed_data.parquet")
    os.remove("/tmp/raw_data.parquet")
