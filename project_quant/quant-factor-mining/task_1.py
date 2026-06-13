from factor_mining import data_acquisition

if "__name__" == "__main__":
    tickers=["AAPL", "MSFT", "GOOGL", "JPM", "XOM",'SPY']
    data = data_acquisition(tickers = tickers)
    

