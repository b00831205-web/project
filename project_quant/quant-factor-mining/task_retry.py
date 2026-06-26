from data_acquisition import retry_batches, merge_checkpoints
import argparse
import os
import pandas as pd


if __name__ == "__main__":
    parse=argparse.ArgumentParser(description="archive raw data using start date and the batch")
    parse.add_argument("--date", type=str, required=True)
    parse.add_argument("--batch", type=str, required=True)
    args=parse.parse_args()

    tmp_dir=os.path.join(os.getcwd(),"tmp")
    checkpoint_dir = os.path.join(tmp_dir, "checkpoint")
    raw_close_path = os.path.join(tmp_dir, "raw_close.parquet")
    raw_volume_path = os.path.join(tmp_dir, "raw_volume.parquet")


    start_date = "2021-01-01"
    close, volume =retry_batches(start_date=start_date, end_date=args.date, max_retries=3)
    if close is not None and volume is not None:
        if os.path.exists(raw_close_path) and os.path.exists(raw_volume_path):
            curr_close = pd.read_parquet(raw_close_path)
            curr_volume = pd.read_parquet(raw_volume_path)
            pd.concat([curr_close, close]).to_parquet(raw_close_path)
            pd.concat([curr_volume, volume]).to_parquet(raw_volume_path)
        else:
            close.to_parquet(raw_close_path)
            volume.to_parquet(raw_volume_path)
        print(f"retry date save to {raw_close_path}, {raw_volume_path}")
    else:
        print("no new data from retry")


