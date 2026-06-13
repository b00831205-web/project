import yfinance as yf
import pandas as pd
import time
import requests
import numpy as np

def data_acquisition(tickers: list, start_date, end_date, useragent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' ) -> pd.Dataframe:
    session = requests.Session()
    session.headers.update({
        'User-Agent': useragent
    })
    
    tickers = tickers #["AAPL", "MSFT", "GOOGL", "JPM", "XOM",'SPY']
    data = {}
    
    for ticker in tickers:
        data[ticker] = yf.download(ticker, start=start_date, end=end_date, 
                                    auto_adjust=True, progress=False, session=session)
        time.sleep(2)  # 每只间隔2秒
    
    # 合并收盘价
    close = pd.DataFrame({t: data[t]["Close"].squeeze() for t in tickers})
    print(close.shape)
    close.head()
    return close


def daily_return(df, tickers):
    daily_return=pd.DataFrame()
    for ticker in tickers:
        daily_return[f'{ticker}']=df[ticker].pct_change()

market_return=daily_return['SPY_daily_return']
excess_return=daily_return.drop(columns=['SPY_daily_return']).sub(market_return, axis=0)
print(excess_return.head())

def momentum(df, ticker:str, tickers: list, day):
    if ticker in tickers:
        current_price=df[ticker]
        start_price=df[ticker].shift(day-1)
        df[f"momentum_{ticker}"]=(start_price-current_price)/start_price
        return df
    
def EWMA(window_data, wk: float): #做.apply()时由于切分下来的nparray会直接传入第一个参数，因此要把window_data写在最前面
    ewma=0
    period = len(window_data)
    for i in range(period):
        ewma += wk**(i-1)*window_data[period-i]
    return ewma
def ShortTermReversal(excess_return: pd.DataFrame,ticker: str, halflife: int, period: int):
    if ticker not in excess_return.columns:
        return None
    wk = (0.5**(1/halflife))
    short_term_reversal=excess_return[ticker].rolling(period).apply(EWMA, raw=True, args=(wk,)) #rolling().apply()传递的是一个长为n的nparray，直接用[]索引
    return -short_term_reversal #反转因子信号是负的——过去收益率高，预期未来会回落

'''
def get_short_term_reversal_ewma(excess_return, ticker, period, halflife):
    if ticker not in excess_return.columns:
        return None
    
    price = excess_return[ticker]
    
    def ewma_func(window):
        weights = np.array([0.5**(1/halflife) ** (len(window) - 1 - i) for i in range(len(window))])
        weights /= weights.sum() #做权重归一化，不做归一化计算出来的EWMA值会受窗口期长短影响——窗口越长，权重之和越大，算出来的值越大，不同窗口期的值没有可比性
        return -np.dot(weights, window)
    
    return price.rolling(period).apply(ewma_func, raw=True)
    '''

def TwentyDayVolatility(daily_return, ticker): #获取20日波动率
    tdv=pd.DataFrame()
    if ticker not in daily_return.column:
        return None
    tdv[ticker]=daily_return[ticker].rolling(20).std()
    return tdv

def TwentyDayNegVotality(daily_return, ticker): #获取20日负收益波动率
    tdnv=pd.DataFrame()
    if ticker not in daily_return.column:
        return "ticker not in the data"
    s = daily_return[ticker]
    neg_return = s.where(s<0) #s.where(cond)的意思是：满足 cond 的保留，不满足的变成NaN
    tdnv[ticker] = neg_return.rolling(window=20, min_period = 1). std()
    return tdnv

def TwentyDayAvgVol(volume, ticker): #20日平均成交量因子
    tdav=pd.DataFrame()
    tdav[ticker]=volume[ticker].rolling(20).mean()
    return tdav

def VolPriceCorr(volume, daily_return, ticker): #20日量价相关系数
    rolling_corr=daily_return[ticker].rolling(20).corr(volume[ticker])
    return rolling_corr