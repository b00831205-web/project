import yfinance as yf
import pandas as pd
import time
import json
import glob

import os

import time
import yfinance as yf
import pandas as pd

def download_batch_with_retry(tickers: list, start_date: str, end_date:str, max_retries:int =3, wait: int =60):
    for attempt in range(max_retries):
        try:
            data = yf.download(tickers, start=start_date, end=end_date,
                               auto_adjust=True, progress=False)
            if data.empty:
                raise ValueError("返回空数据")
            return data
        except Exception as e:
            print(f"第{attempt+1}次失败: {e}")
            if attempt < max_retries - 1:
                print(f"等待{wait}秒后重试...")
                time.sleep(wait)
    return None    

def data_aquisition(tickers:list, start_date:str, end_date:str, batch_size:int, 
                    max_retries: int =3, wait: int = 60, checkpoint_dir: str = "tmp/checkpoint") -> pd.DataFrame:
    close=[]
    volume=[]
    os.makedirs(checkpoint_dir, exist_ok=True)
    def download_batch_with_retry(batch: list, start_date: str, end_date:str, batch_index:int  ,max_retries:int =3, wait: int =60) ->pd.DataFrame | None :
        checkpoint_path = os.path.join(checkpoint_dir, f"batch_{batch_index}.parquet")
        if os.path.exists(checkpoint_path):
            print(f"{batch_index} already exist")
            return 

        for attempt in range(max_retries):
            try:
                data = yf.download(batch, start=start_date, end=end_date,
                                auto_adjust=True, progress=False)
                if data.empty:
                    raise ValueError("返回空数据")
                data.to_parquet(checkpoint_path)
                return data
            except Exception as e:
                print(f"第{attempt+1}次失败: {e}")
                if attempt < max_retries - 1:
                    print(f"等待{wait}秒后重试...")
                    time.sleep(wait)
        with open(os.path.join(checkpoint_dir, "failed_batches.json"), mode= "a") as f:
            json.dump({"batch_index":batch_index, "tickers":batch}, f)
            f.write("\n")
        print(f"batch {batch_index} failed, logging to {os.path.join(checkpoint_dir, 'failed_batches.json')}")    
        return None    
    
    all_close = []
    all_volume = []
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i: i+batch_size]
        batch_index= i//batch_size+1
        print(f"downloading batch{batch_index} ... \ntickers {i} - {min(len(tickers), {i+batch_size})}")
        data = download_batch_with_retry(batch=batch, start_date=start_date, end_date=end_date, max_retries=max_retries, wait=wait, batch_index=batch_index)
        if data is not None:
            if isinstance(data.columns, pd.MultiIndex):
                all_close.append(data['Close'])
                all_volume.append(data['Volume'])
        time.sleep(10)
    
    close = pd.concat(all_close, axis=1)
    volume = pd.concat(all_volume, axis=1)
    return close, volume

def retry_batches(start_date: str, end_date: str, max_retries: int, checkpoint_dir: str = "tmp\checkpoint", wait: int =60)->pd.DataFrame | None:
    failed_log = os.path.join(checkpoint_dir, "failed_batches.json")
    retry_log = os.path.join(checkpoint_dir, "retry_log.json")
    if not os.path.exists(failed_log):
        print("no failed batches need to be proceeded")
        return None
    failed = []
    with open(failed_log) as f:
        for line in f:
            failed.append(json.load(line))

    retry_count = 1
    if os.path.exists(retry_log):
        with open(retry_log) as f:
            records = [json.load(line) for line in f if line.strip()]
            if records:
                retry_count = records[-1]["retry_call"] +1
    print(f"{retry_count}th retrying, {len(failed)} totally failed")

    
    still_failed=[]
    retry_records = []
    for record in failed:
        batch_index = record["batch_index"]
        batch = record["tickers"]
        checkpoint_path = os.path.join(checkpoint_dir, f"batch_{batch_index}.parquet")
        
        print(f"retring {batch_index}")
        success = False
        for attempt in range(max_retries):
            try:
                data = yf.download(batch, start=start_date, end=end_date,
                                auto_adjust=True, progress=False)
                if data.empty:
                    raise ValueError("返回空数据")
                retry_records.append({
                    "retry_call":retry_count,
                    "batch_index": batch_index,
                    "status": "success",
                    "attempts": attempt + 1
                })
                print(f"{batch} successed!")
                success = True
                break
            except Exception as e:
                print(f"第{attempt+1}次失败: {e}")
                if attempt < max_retries - 1:
                    print(f"等待{wait}秒后重试...")
                    time.sleep(wait)
        if not success:
            print(f"batch {batch} still download failed")
            retry_records.append({
                    "retry_call":retry_count,
                    "batch_index": batch_index,
                    "status": "failed",
                    "attempts": max_retries
                })
            still_failed.append(record)
        with open(failed_log, "w") as f:
            for record in still_failed:
                json.dump(record, f)
                f.write("\n")

        with open(retry_log, "a") as f:
            for record in retry_records:
                json.dump(record, f)
                f.write("\n")
        if still_failed:
            print(f"still {len(still_failed)} failed downloading")
        else:
            print("all the failed downloading successed")

def merge_checkpoints(checkpoint_dir: str = "tmp/checkpoint") -> tuple:
    """把所有批次的检查点文件合并成完整的 close 和 volume"""
    files = sorted(glob.glob(os.path.join(checkpoint_dir, "batch_*.parquet")),
                   key=lambda x: int(x.split("batch_")[1].split(".")[0]))
    
    all_close, all_volume = [], []
    for f in files:
        data = pd.read_parquet(f)
        if isinstance(data.columns, pd.MultiIndex):
            all_close.append(data["Close"])
            all_volume.append(data["Volume"])
    
    close = pd.concat(all_close, axis=1)
    volume = pd.concat(all_volume, axis=1)
    return close, volume