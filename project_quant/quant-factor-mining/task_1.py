from factor_mining import data_acquisition
import argparse
import datetime
import os
import pandas as pd


if __name__ == "__main__":
    parse=argparse.ArgumentParser(description="archive raw data using start date and the batch")
    parse.add_argument("--date", type=str, required=True)
    parse.add_argument("--batch", type=str, required=True)
    args=parse.parse_args()

    base_dir=os.getcwd()
    tmp_dir = os.path.join(base_dir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    raw_close_path=os.path.join(tmp_dir, "raw_close.parquet")
    raw_volume_path=os.path.join(tmp_dir, "raw_volume.parquet")
    
    close_path=os.path.join(tmp_dir, "close.parquet")
    volume_path=os.path.join(tmp_dir, "volume.parquet")
    
    end_date=args.date
    tickers=["AAPL", "MSFT", "GOOGL", "JPM", "XOM",'SPY']

    if os.path.exists(close_path) and os.path.exists(volume_path):
        existing_close = pd.read_parquet(close_path)
        existing_volume = pd.read_parquet(volume_path)
        last_date = min(existing_close.index.max(),existing_volume.index.max())
        start_date=((last_date + datetime.timedelta(days=1))).strftime("%Y-%m-%d")
    else:
        start_date="2021-01-01"
    
    if start_date >= end_date:
        print(f"{args.batch} is newest, no need to be updated")
    else:   
        close, volume =data_acquisition(tickers = tickers, start_date=start_date, end_date=end_date)
        close.to_parquet(os.path.join(tmp_dir, "raw_close.parquet"))
        volume.to_parquet(os.path.join(tmp_dir, "raw_volume.parquet"))
        print(f"data has been download to temp path {raw_close_path}, {raw_volume_path}")
    

