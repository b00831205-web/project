from data_acquisition import data_acquisition
import argparse
import datetime
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    
    close_path=os.path.join(tmp_dir, "close.parquet")
    volume_path=os.path.join(tmp_dir, "volume.parquet")
    
    r = requests.get(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    tickers = [
        row.find('td').get_text(strip=True)
        for row in table.find('tbody').find_all('tr')[1:]
        if row.find('td')
    ]
    # Yahoo Finance 格式：BRK.B → BRK-B
    tickers = [t.replace('.', '-') for t in tickers]
    tickers.append('SPY')  # 保留基准，删掉这行如果不需要
    print(f"Loaded {len(tickers)} tickers")

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
        close, volume =data_acquisition(tickers = tickers, start_date=start_date, end_date=end_date, batch_size=50)
        close.to_parquet(os.path.join(tmp_dir, "raw_close.parquet"))
        volume.to_parquet(os.path.join(tmp_dir, "raw_volume.parquet"))
        print(f"data has been download to temp path {raw_close_path}, {raw_volume_path}")
    

