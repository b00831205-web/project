import pandas as pd


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
    mmt={}
    for ticker in tickers:
        current_price=df[ticker]
        start_price=df[ticker].shift(day-1)
        mmt[f"{day}DayMomentum_{ticker}"]=(current_price-start_price)/start_price
    mmt = pd.DataFrame(mmt)
    return mmt
    
def EWMA(window_data, wk: float)->float: #做.apply()时由于切分下来的nparray会直接传入第一个参数，因此要把window_data写在最前面
    ewma=0
    period = len(window_data)
    for i in range(period):
        ewma += wk**(i)*window_data[period-i-1]
    return ewma

def ShortTermReversal(excess_return: pd.DataFrame,tickers: list, halflife: int, period: int)->pd.DataFrame:
    short_term_reversal={}
    for ticker in tickers:
        if ticker not in excess_return.columns:
            continue
        wk = (0.5**(1/halflife))
        short_term_reversal[ticker]=-excess_return[ticker].rolling(period).apply(EWMA, raw=True, args=(wk,)) #rolling().apply()传递的是一个长为n的nparray，直接用[]索引
    short_term_reversal = pd.DataFrame(short_term_reversal)
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
    tdv={}
    for ticker in tickers:
        if ticker not in daily_return.columns:
            continue
        tdv[ticker]=daily_return[ticker].rolling(20).std()
    tdv = pd.DataFrame(tdv)
    return tdv

def TwentyDayNegVotality(daily_return:pd.DataFrame, tickers:list)->pd.DataFrame: #获取20日负收益波动率
    tdnv={}
    for ticker in tickers:
        if ticker not in daily_return.columns:
            continue
        s = daily_return[ticker]
        neg_return = s.where(s<0) #s.where(cond)的意思是：满足 cond 的保留，不满足的变成NaN
        tdnv[ticker] = neg_return.rolling(window=20, min_periods = 1). std()
    tdnv = pd.DataFrame(tdnv)
    return tdnv

def TwentyDayAvgVol(volume:pd.DataFrame, tickers:list)->pd.DataFrame: #20日平均成交量因子
    rolling_tdav_dict={}
    for ticker in tickers:
        rolling_tdav_dict[ticker]=volume[ticker].rolling(20).mean()
    rolling_tdav_dict = pd.DataFrame(rolling_tdav_dict)
    return rolling_tdav_dict

def VolPriceCorr(volume:pd.DataFrame, daily_return:pd.DataFrame, tickers:list)->pd.DataFrame: #20日量价相关系数
    rolling_corr_dict = {}
    for ticker in tickers:
        rolling_corr_dict[ticker] = daily_return[ticker].rolling(20).corr(volume[ticker])
    rolling_corr = pd.DataFrame(rolling_corr_dict)
    return rolling_corr