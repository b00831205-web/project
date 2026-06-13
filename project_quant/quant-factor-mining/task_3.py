import pandas as pd

if "__name__"=="__main__":
    df = pd.DataFrame(pd.read_parquet("/tmp/proceed_data.parquet"))
    df 
    