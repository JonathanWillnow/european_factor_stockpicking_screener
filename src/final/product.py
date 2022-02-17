import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool
from datetime import datetime
import time
import numpy as np
import pandas as pd
import random
from pandas import ExcelWriter
from bs4 import BeautifulSoup
from scipy import stats #The SciPy stats module
import math #The Python math module

def get_european_weights_ken_french():
    from pandas_datareader.famafrench import get_available_datasets
    import pandas_datareader.data as web

    # default factor allocation due to past 6 months performance??!!
    # -14 since factors come available with 2 months delay
    # s_START_DATE = str(datetime.today().strftime("%Y-%m-%d").AddMonths(-8))
    # s_END_DATE = str(datetime.today().strftime("%Y-%m-%d"))

    START_DATE = '2000-05-01'
    END_DATE = '2022-01-22'

    ff_dict = web.DataReader('Europe_5_Factors', 'famafrench', start=START_DATE, end = END_DATE) # default is monthly  #ff_dict.keys()  #print(ff_dict["DESCR"])
    factor_df = ff_dict[0]#monthly factors. 1 for annual
    factor_df.rename(columns = {"Mkt-RF": "mkt_rf", "SMB":"smb", "HML":"hml", "RMW":"rmw", "CMA":"cma", "RF":"rf"}, inplace= True) 
    factor_df["mkt"] = factor_df.mkt_rf + factor_df.rf
    factor_df = factor_df.apply(pd.to_numeric, errors='coerce').div(100)
    #meandf = factor_df[["smb", "hml", "rmw", "cma"]].mean()*100
    adjust_weights = factor_df[["smb", "hml", "rmw", "cma"]].mean()*100
    return(adjust_weights.values)


def calculate_precentiles(rv_dataframe):
    from statistics import mean
    metrics = {
            'enterpriseValue': 'EV_percentile',
            'priceToSalesTrailing12Months' : 'PS_percentile',
            }


    FF_metrics = {
            'marketCap': 'MC_percentile',
            'priceToBook':'PB_percentile',
            'FF_Quality_mean' : 'FFQ(inv)_m_percentile',
            #'FF_Quality_Growth' : 'FFQ(inv)_g_percentile',
            'FF_Assets_Growth_mean': 'FFA_m_percentile',
    }
    weights = [100,1,1]
    ff_weights = get_european_weights_ken_french()
    print(ff_weights)
    for row in rv_dataframe.index:
        value_percentiles = []
        for i, metric in enumerate(FF_metrics.keys()):
            value_percentiles.append(rv_dataframe.loc[row, FF_metrics[metric]] * ff_weights[i])
        rv_dataframe.loc[row, 'RV Score'] = sum(value_percentiles) / sum(ff_weights)
        
    return rv_dataframe

