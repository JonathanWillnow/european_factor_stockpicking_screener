import urllib.request, json , time, os, difflib, itertools
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool
from datetime import datetime
import time
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
from pandas import ExcelWriter
from bs4 import BeautifulSoup
from scipy import stats #The SciPy stats module
import datetime


# https://www.reddit.com/r/sheets/comments/ji52uk/yahoo_finance_api_url/ available modules xahoo finance



metrics_list = ['enterpriseValue', "marketCap",'forwardPE', "trailingPE", 'profitMargins', 'floatShares', 'priceToBook', 'heldPercentInsiders',
                'bookValue', 'priceToSalesTrailing12Months', 'trailingEps', 'forwardEps',
                'pegRatio', 'enterpriseToRevenue', 'enterpriseToEbitda']

financial_list = ["currentPrice","quickRatio","currentRatio", "debtToEquity", "returnOnAssets", "returnOnEquity",
                   "revenueGrowth", "grossMargins", "ebitdaMargins", "operatingMargins", "profitMargins"]# "PB_percentile", "EV_percentile", "PS_percentile"]

check_list = ['forwardPE', "trailingPE", "marketCap", 'priceToSalesTrailing12Months']



#https://link.springer.com/article/10.1007/s41464-020-00105-y
#The operating profitability (OP) according to Fama and French (2015) is calculated using all accounting numbers from the end of the previous fiscal year. 
#It is defined by the annual revenues minus the cost of goods sold, interest expenses, selling, general, and administrative expenses divided by the book equity. 

def get_data():
    final_frame = pd.DataFrame({})
    stocklist = ["BC8.DE"]
    for stock in stocklist:
    
    #for tckr in ticker_data.ticker:
        data_dict = {}
        data_dict["Ticker"] = stock
        data_dict["date"] = datetime.datetime.today().strftime("%Y-%m-%d")
        try:
            #stock = str(tckr) + ".F"
            query_url_1= "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=defaultKeyStatistics"

            with urllib.request.urlopen(query_url_1) as url:
                        parsed_1 = json.loads(url.read().decode())
        except:
            try:
                #stock = str(tckr) + ".DE"
                query_url_1= "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=defaultKeyStatistics"

                with urllib.request.urlopen(query_url_1) as url:
                            parsed_1 = json.loads(url.read().decode())
            except:
                continue
                
        for metric in metrics_list:
            try:
                data_dict[metric] = parsed_1["quoteSummary"]["result"][0]['defaultKeyStatistics'][metric]["raw"]
            except:
                data_dict[metric] = np.nan

        ####################################################################
        query_url_2 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=financialData"

        with urllib.request.urlopen(query_url_2) as url:
                    parsed_2 = json.loads(url.read().decode())

        for metric in financial_list:
            try:
                data_dict[metric] = parsed_2["quoteSummary"]["result"][0]['financialData'][metric]["raw"]
            except:
                data_dict[metric] = np.nan
        
        # dict["EV"] = parsed["quoteSummary"]["result"][0]['defaultKeyStatistics']['enterpriseValue']["raw"]
        # dict["PE"] = parsed["quoteSummary"]["result"][0]['defaultKeyStatistics']['forwardPE']["raw"]
        # dict["ProfitMargins"] = parsed["quoteSummary"]["result"][0]['defaultKeyStatistics']['profitMargins']["raw"]
        # dict["Float"] = parsed["quoteSummary"]["result"][0]['defaultKeyStatistics']['floatShares']["raw"]
        # dict["PB"] = parsed["quoteSummary"]["result"][0]['defaultKeyStatistics']['priceToBook']["raw"]

       
        for metric in check_list:
            try:
                if np.isnan(dict[metric]):
                    query_url_3 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=summaryDetail"
                    with urllib.request.urlopen(query_url_3) as url:
                            parsed_3 = json.loads(url.read().decode())
                    data_dict[metric] = parsed_3["quoteSummary"]["result"][0]["summaryDetail"][metric]["raw"]
            except:
                pass


        

        frame = pd.DataFrame.from_dict({stock : data_dict}, orient="index")
        final_frame = final_frame.append(frame)


    


    
    return(final_frame)