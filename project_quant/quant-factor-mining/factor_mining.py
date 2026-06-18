import yfinance as yf
import pandas as pd
import time
import numpy as np
import datetime

import requests

def download_yahoo(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    period1 = int(pd.Timestamp(start_date).timestamp())
    period2 = int(pd.Timestamp(end_date).timestamp())
    
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
    params = {
        'period1': period1,
        'period2': period2,
        'interval': '1d',
        'events': 'history'
    }
    
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    
    result = data['chart']['result'][0]
    if "timestamp" not in result:
        print(f"{ticker} no data")
        return None
    timestamps = result['timestamp']
    quote = result['indicators']['quote'][0]
    adjclose = result['indicators'].get('adjclose', [{}])[0].get('adjclose', quote['close'])
    
    df = pd.DataFrame({
        'Open': quote['open'],
        'High': quote['high'],
        'Low': quote['low'],
        'Close': adjclose,
        'Volume': quote['volume']
    }, index=pd.to_datetime(timestamps, unit='s').date)
    
    df.index.name = 'Date'
    return df


def data_acquisition(tickers: list, start_date="2020-01-01", end_date=None)->pd.DataFrame:
    close = pd.DataFrame()
    volume = pd.DataFrame()
    for ticker in tickers:
        df = download_yahoo(ticker, start_date, end_date)
        if df is not None:
            close[ticker] = df['Close']
            volume[ticker] = df['Volume']
        time.sleep(2)
    return close, volume
    


def daily_return(df:pd.DataFrame, tickers:list)->pd.DataFrame:
    daily_return=pd.DataFrame()
    for ticker in tickers:
        daily_return[f'{ticker}']=df[ticker].pct_change()
    return daily_return

def excess_return(daily_return: pd.DataFrame) -> pd.DataFrame:
    market_return=daily_return['SPY']
    excess_return=daily_return.drop(columns=['SPY']).sub(market_return, axis=0)
    return excess_return

def momentum(df: pd.DataFrame, tickers: list, day:int =2) -> pd.DataFrame:
    mmt=pd.DataFrame()
    for ticker in tickers:
        current_price=df[ticker]
        start_price=df[ticker].shift(day-1)
        mmt[f"momentum_{ticker}"]=(start_price-current_price)/start_price
    return mmt
    
def EWMA(window_data, wk: float)->float: #做.apply()时由于切分下来的nparray会直接传入第一个参数，因此要把window_data写在最前面
    ewma=0
    period = len(window_data)
    for i in range(period):
        ewma += wk**(i-1)*window_data[period-i-1]
    return ewma

def ShortTermReversal(excess_return: pd.DataFrame,tickers: list, halflife: int, period: int)->pd.DataFrame:
    short_term_reversal=pd.DataFrame()
    for ticker in tickers:
        if ticker not in excess_return.columns:
            continue
        wk = (0.5**(1/halflife))
        short_term_reversal[ticker]=-excess_return[ticker].rolling(period).apply(EWMA, raw=True, args=(wk,)) #rolling().apply()传递的是一个长为n的nparray，直接用[]索引
    return short_term_reversal #反转因子信号是负的——过去收益率高，预期未来会回落

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

def TwentyDayVolatility(daily_return:pd.DataFrame, tickers:list)->pd.DataFrame: #获取20日波动率
    tdv=pd.DataFrame()
    for ticker in tickers:
        if ticker not in daily_return.columns:
            continue
        tdv[ticker]=daily_return[ticker].rolling(20).std()
    return tdv

def TwentyDayNegVotality(daily_return:pd.DataFrame, tickers:list)->pd.DataFrame: #获取20日负收益波动率
    tdnv=pd.DataFrame()
    for ticker in tickers:
        if ticker not in daily_return.columns:
            continue
        s = daily_return[ticker]
        neg_return = s.where(s<0) #s.where(cond)的意思是：满足 cond 的保留，不满足的变成NaN
        tdnv[ticker] = neg_return.rolling(window=20, min_periods = 1). std()
    return tdnv

def TwentyDayAvgVol(volume:pd.DataFrame, tickers:list)->pd.DataFrame: #20日平均成交量因子
    tdav=pd.DataFrame()
    for ticker in tickers:
        tdav[ticker]=volume[ticker].rolling(20).mean()
    return tdav

def VolPriceCorr(volume:pd.DataFrame, daily_return:pd.DataFrame, tickers:list)->pd.DataFrame: #20日量价相关系数
    rolling_corr=pd.DataFrame()
    for ticker in tickers:
        rolling_corr[ticker]=daily_return[ticker].rolling(20).corr(volume[ticker])
    return rolling_corr