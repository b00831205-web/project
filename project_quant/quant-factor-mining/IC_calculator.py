import pandas as pd
import os
from scipy import stats
import numpy as np

def different_holding_period(close:pd.DataFrame, tickers: list, periods: list | int)->pd.DataFrame:
    different_holding=pd.DataFrame()
    for ticker in tickers:
        for period in periods:    
            different_holding[f"{period}DaysHoldingPeriod_{ticker}"] = close[ticker].pct_change(period).shift(-period)
    return different_holding

def data_standarization(df:pd.DataFrame)->pd.DataFrame:
    factors = list(set(cols.rsplit("_",1)[0] for cols in df.columns))
    tickers = list(set(cols.rsplit("_",1)[1] for cols in df.columns))
    temp = pd.DataFrame()
    for factor in factors:
        cols = [f'{factor}_{ticker}' for ticker in tickers]
        cols = [c for c in cols if c in df.columns]
        truncate_data=df[cols]
        ranked = truncate_data.rank(axis=1,pct=True)*2-1
        temp[cols]=ranked

            #truncate_data.iloc[index] = truncate_data.iloc[index]/truncate_data.iloc[index].max()，最大值归一化受极端值影响大，不建议使用
    return temp

def TM_Information_correlation(tickers : list, factors: pd.DataFrame, different_holding_period: pd.DataFrame, output_path=str)->pd.DataFrame:
    TM_IC_matrix=pd.DataFrame() #时序IC
    
    def ticker_dict(tickers: list, df:pd.DataFrame)->dict:
        tickers_dict={ticker:[] for ticker in tickers}
        for ticker in tickers:
            for column in df.columns:
                if column.rsplit("_",1)[1] == ticker:
                    tickers_dict[ticker].append(column)
        return tickers_dict
    
    ticker_factor_dict={}
    for ticker, factor in ticker_dict(tickers, factors).items():
        if factor:
            df = factors[factor].copy()
            df.columns=[c.rsplit('_',1)[0] for c in factor]
            ticker_factor_dict[ticker] = df
    
    ticker_holding_dict={}
    for ticker, holding_period in ticker_dict(tickers, different_holding_period).items():
        if holding_period:
            df = different_holding_period[holding_period].copy()
            df.columns=[c.rsplit('_',1)[0] for c in holding_period]
            ticker_holding_dict[ticker] = df
    
    result=[]
    for ticker, factor in ticker_factor_dict.items():
        holding_df =ticker_holding_dict[ticker]
        for h_col in holding_df.columns:
            ic = factor.corrwith(holding_df[h_col],method="pearson",axis =0)
            ic.name=f'{ticker}_{h_col}'
            result.append(ic)
    TM_IC_matrix = pd.concat(result,axis=1)
    
    TM_IC_matrix.to_parquet(os.path.join(os.getcwd(), output_path))
    print("Time Series Information Correlation computation complete")

    return TM_IC_matrix

def CS_Information_Correlation(factors:pd.DataFrame, different_holding_period: pd.DataFrame, output_path: str)-> pd.DataFrame:
    CS_IC_matrix=pd.DataFrame() #截面IC
    
    #获取ticker和因子列表
    ticker_list=[]
    factor_list=[]
    for column in factors.columns:
        factor, ticker = column.rsplit("_",1)
        factor_list.append(factor)
        ticker_list.append(ticker)
    factor_list=list(set(factor_list))
    ticker_list=list(set(ticker_list))
    
    #获取持有期列表
    holding_period_list =[]
    for column in different_holding_period.columns:
        holding_period, ticker = column.rsplit("_",1)
        holding_period_list.append(holding_period)
    holding_period_list = list(set(holding_period_list))
    
    def factor_dict(factors: list, df:pd.DataFrame) ->dict:
        factors_dict={factor: [] for factor in factors}
        for factor in factors:
            for column in df.columns:
                if column.rsplit("_",1)[0] == factor:
                    factors_dict[factor].append(column)
        return factors_dict
    
    ticker_factor_dict={}
    for factor, ticker in factor_dict(factor_list, factors).items():
        if ticker:
            df = factors[ticker].copy()
            df.columns=[c.rsplit('_',1)[1] for c in ticker]
            ticker_factor_dict[factor] = df
    
    ticker_holding_dict={}
    for holding_period, ticker in factor_dict(holding_period_list, different_holding_period).items():
        if ticker:
            df = different_holding_period[ticker].copy()
            df.columns=[c.rsplit('_',1)[1] for c in ticker]
            ticker_holding_dict[holding_period] = df

    result=[]
    for factor, factor_df in ticker_factor_dict.items():
        for holding_period , holding_period_ticker in ticker_holding_dict.items():
            ic_series= factor_df.corrwith(holding_period_ticker[factor_df.columns], method='pearson',axis=1)
            ic_series.name=f"{factor}_{holding_period}"
            result.append(ic_series)
    CS_IC_matrix=pd.concat(result, axis=1)

    CS_IC_matrix.to_parquet(os.path.join(os.getcwd(), output_path))
    print("Cross Section Information Correlation computation complete")

    return CS_IC_matrix

def summary(cross_section_IC_matrix:pd.DataFrame)->pd.DataFrame:
    return pd.DataFrame({
        'IC_mean' : cross_section_IC_matrix.mean(),
        'IC_std': cross_section_IC_matrix.std(),
        'IR': cross_section_IC_matrix.mean()/cross_section_IC_matrix.std(),
        'IC>0 pct': (cross_section_IC_matrix>0).mean(),
        'n': cross_section_IC_matrix.count(),
    })

def multiple_testing(cross_section_IC_matrix_summary:pd.DataFrame)->pd.DataFrame:
    significant_t = pd.DataFrame({
        "t":cross_section_IC_matrix_summary["IR"]*np.sqrt(cross_section_IC_matrix_summary["n"]),
        "p_value":stats.t.sf(x=cross_section_IC_matrix_summary["IR"]*cross_section_IC_matrix_summary["n"],df=cross_section_IC_matrix_summary["n"])
        })
    significant_t['significant'] = "True" if significant_t['p_value'] < stats.t.sf(x=0.05, df=cross_section_IC_matrix_summary['n']) else "False"
    significant_t['Bonferroni_p-value'] = stats.t.sf(x=0.05/cross_section_IC_matrix_summary['n'], df=cross_section_IC_matrix_summary)
    significant_t['Bonferroni_significant'] = "True" if significant_t['p_value'] < stats.t.sf(x=0.05/cross_section_IC_matrix_summary['n'], df=cross_section_IC_matrix_summary) else "False"
    significant_t['Rank'] = significant_t.sort_values(by="p_value").rank(ascending=0,method='max')
    significant_t['BH_p-value'] = stats.t.sf(x=significant_t['Rank']/cross_section_IC_matrix_summary['n']*0.05, df=cross_section_IC_matrix_summary['n'])
    significant_t['BH_significant'] = "True" if significant_t['p_value'] < stats.t.sf(x=significant_t['Rank']/cross_section_IC_matrix_summary['n']*0.05, df=cross_section_IC_matrix_summary['n']) else "False"

def orthogonal_analysis(factors_ticker: pd.DataFrame):
    factors = list(set(col.rsplit('_',1)[0] for col in factors_ticker.columns))
    tickers = list(set(col.rsplit('_',1)[1] for col in factors_ticker.columns))
    corr_accumulator = pd.DataFrame(0.0, index = factors, columns=factors)
    valid_days=0
    for date in factors_ticker.index:
        row = factors_ticker.loc[date]
        cross_section_daily = pd.DataFrame({
            factor: pd.Series({
                ticker: row[f'{factor}_{ticker}'] 
                for ticker in tickers 
                if f"{factor}_{ticker}" in factors_ticker.columns
                })
            for factor in factors
        }, index=tickers)
        
        if cross_section_daily.isnull().all().any(): #500*8 bool矩阵，每个值是否为NaN，对每列，是否全部都是NaN（返回一个长度为8的series），这8列中，是否有至少一列全是NaN
            continue
        
        corr_accumulator += cross_section_daily.corr() #corr计算所有数据所有列间的相关性系数
        valid_days+=1
    avg_corr = corr_accumulator/valid_days
    high_corr_dict={
        column: (avg_corr[column]>0.5).index for column in avg_corr.columns 
    }
    return avg_corr


def rolling_IC(factors:pd.DataFrame, different_holding_period: pd.DataFrame)-> pd.DataFrame:
    factors.rolling(126).corrwith()

if __name__=='__main__':
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    close_data=pd.read_parquet("tmp/close.parquet")
    factor_data=pd.read_parquet("tmp/factors.parquet")
    
    orth_result=orthogonal_analysis(factors_ticker=factor_data)
    print(orth_result)


    # ticker_list=close_data.columns
    # periods=[1,5,20]
    
    # different_holding_period_df = data_standarization(different_holding_period(close=close_data, tickers=ticker_list, periods=periods))
    
    # tm_output = "tmp/TM_IC.parquet"
    # cs_output = "tmp/CS_IC.parquet"
    # factor_data = data_standarization(factor_data)
    
    
    # time_series_IC = TM_Information_correlation(tickers=ticker_list, factors=factor_data, different_holding_period=different_holding_period_df, output_path=tm_output)
    # cross_section_IC = CS_Information_Correlation(factors=factor_data, different_holding_period=different_holding_period_df, output_path=cs_output)

    # print(pd.read_parquet("tmp/CS_IC.parquet"))
    # print(summary(cross_section_IC_matrix=cross_section_IC))
    