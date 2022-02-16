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
stockinfo_csv = pd.read_csv("fama_french/data/StoxxEurope600.csv")  
def get_data(stockticker):
    metrics_list = ['enterpriseValue', "marketCap",'forwardPE', "trailingPE", 'profitMargins', 'floatShares', "sharesOutstanding", 
                    'priceToBook', 'heldPercentInsiders', 'bookValue', 'priceToSalesTrailing12Months', 'trailingEps', 'forwardEps',
                    'pegRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', "dividendYield"]

    financial_list = ["currentPrice","quickRatio","currentRatio", "debtToEquity", "returnOnAssets", "returnOnEquity",
                    "revenueGrowth", "grossMargins", "ebitdaMargins", "operatingMargins", "profitMargins"]# "PB_percentile", "EV_percentile", "PS_percentile"]

    check_list = ['forwardPE', "trailingPE", "marketCap", 'priceToSalesTrailing12Months', "dividendYield"]

    Fame_French_Quality = ["totalRevenue", "costOfRevenue", "grossProfit", "sellingGeneralAdministrative", "interestExpense", "operatingIncome", "netIncomeFromContinuingOps"]
    
    #get exchange
    #countrycode = stockinfo.ISIN[stockinfo.ticker == stockticker].values[0][:2]
   
    stock = str(stockticker) #+ ".F"
    data_dict = {}
    data_dict["ticker"] = stock
    data_dict["date"] = datetime.today().strftime("%Y-%m-%d")
    try:
        query_url_1= "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=defaultKeyStatistics"

        with urllib.request.urlopen(query_url_1) as url:
                    parsed_1 = json.loads(url.read().decode())
        data_dict["industry"] = stockinfo_csv.industry[stockinfo_csv.ticker == stockticker].values[0]
        data_dict["de_ticker"] = stockinfo_csv.de_ticker[stockinfo_csv.ticker == stockticker].values[0]
    except Exception as e:
        print(e)
        print(stockticker)
        data_dict["industry"] = np.nan
        data_dict["de_ticker"] = np.nan

    for metric in metrics_list:
        try:
            data_dict[metric] = parsed_1["quoteSummary"]["result"][0]['defaultKeyStatistics'][metric]["raw"]
        except:
            data_dict[metric] = np.nan

    try:
        query_url_2 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=financialData"

        with urllib.request.urlopen(query_url_2) as url:
                    parsed_2 = json.loads(url.read().decode())
    except Exception as e:
        print(e)
        print(stockticker)

    for metric in financial_list:
        try:
            data_dict[metric] = parsed_2["quoteSummary"]["result"][0]['financialData'][metric]["raw"]
        except:
            data_dict[metric] = np.nan

    for metric in check_list:
        if np.isnan(data_dict[metric]):
            try:
                query_url_3 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=summaryDetail"
                with urllib.request.urlopen(query_url_3) as url:
                        parsed_3 = json.loads(url.read().decode())
                data_dict[metric] = parsed_3["quoteSummary"]["result"][0]["summaryDetail"][metric]["raw"]
            except:
                pass
    ## FF Quality
    Fame_French_Quality = ["totalRevenue", "costOfRevenue", "grossProfit", "sellingGeneralAdministrative", "interestExpense", "operatingIncome", "netIncomeFromContinuingOps"]
    
    FF_Quality_dict = {}
    FF_Quality_year_frame = pd.DataFrame({})
    try:
        query_url_4 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=incomeStatementHistory"
        with urllib.request.urlopen(query_url_4) as url:
                    parsed_4 = json.loads(url.read().decode())

        query_url_5 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=balanceSheetHistory"
        with urllib.request.urlopen(query_url_5) as url:
                    parsed_5 = json.loads(url.read().decode())
    except Exception as e:
        print(e)
        print(stockticker)

    for year in range(0,10):
        try:
            for metric in Fame_French_Quality:
                FF_Quality_dict[metric] = parsed_4["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][year][metric]["raw"]
            FF_Quality_dict["totalStockholderEquity"] = parsed_5["quoteSummary"]["result"][0]["balanceSheetHistory"]["balanceSheetStatements"][year]["totalStockholderEquity"]["raw"]
            FF_Quality_dict["year"] = year 
            # Building FF-Quality Factor 
            FF_Quality_dict["FF_Quality"] = (FF_Quality_dict["totalRevenue"] - (FF_Quality_dict["costOfRevenue"] + FF_Quality_dict["interestExpense"] + FF_Quality_dict["sellingGeneralAdministrative"])) / FF_Quality_dict["totalStockholderEquity"]
            FF_Quality_frame = pd.DataFrame.from_dict({stock : FF_Quality_dict}, orient="index")
            FF_Quality_year_frame = FF_Quality_year_frame.append(FF_Quality_frame)
        except:
            break

    # Calculate Growth rates and report recent and mean FF_Quality Factor
    data_dict["years_available"] = len(FF_Quality_year_frame)
    growth_measures_dict = {
        "RevGrowth":"totalRevenue",
        "GrossProfitGrowth": "grossProfit",
        "OpIncomeGrowth" : "operatingIncome",
        "FF_Quality_Growth": "FF_Quality",
    }
    for measure in growth_measures_dict:
        try:
            data_dict[measure] = FF_Quality_year_frame.sort_values(["year"], ascending=False)[[growth_measures_dict[measure]]].pct_change().mean()[0]
        except:
            data_dict[measure] = np.nan

    try:
        data_dict["FF_Quality_actual"] = FF_Quality_year_frame[FF_Quality_year_frame.year == 0].FF_Quality[0]
        data_dict["FF_Quality_mean"] = FF_Quality_year_frame.FF_Quality.mean()
    except:
        data_dict["FF_Quality_actual"] = np.nan
        data_dict["FF_Quality_mean"] = np.nan

    
    FF_Conservative_dict = {}
    FF_Conservative_year_frame = pd.DataFrame({})
    # FF Inv
    for year in range(0,10):
        try:
            FF_Conservative_dict["totalAssets"] = parsed_5["quoteSummary"]["result"][0]["balanceSheetHistory"]["balanceSheetStatements"][year]["totalAssets"]["raw"]
            FF_Conservative_dict["year"] = year 
            FF_Conservative_frame = pd.DataFrame.from_dict({stock : FF_Conservative_dict}, orient="index")
            FF_Conservative_year_frame = FF_Conservative_year_frame.append(FF_Conservative_frame)
        except:
            break
    try:
        data_dict["FF_Assets_Growth_mean"] = FF_Conservative_year_frame.sort_values(["year"], ascending=False)[["totalAssets"]].pct_change().mean()[0]
        data_dict["FF_Assets_Growth_actual"] = FF_Conservative_year_frame.sort_values(["year"], ascending=False)[["totalAssets"]].pct_change().iloc[1,0]
    except:
        data_dict["FF_Assets_Growth_mean"] = np.nan
        data_dict["FF_Assets_Growth_actual"] = np.nan


    frame = pd.DataFrame.from_dict({stock : data_dict}, orient="index")

    return(frame)


def calc_precentiles(final_frame):

    metrics = {
            'priceToBook':'PB_percentile',
            'enterpriseValue': 'EV_percentile',
            'priceToSalesTrailing12Months' : 'PS_percentile',
            'enterpriseToRevenue' : "EToRev_precentile",
            'enterpriseToEbitda' : "EToEbitda_percentile",
            }

    for row in final_frame.index:
        for metric in metrics.keys():
            final_frame.loc[row, metrics[metric]] = stats.percentileofscore(final_frame[metric], final_frame.loc[row, metric])/100
    
       # metrics where we have to invert the percentile
    inv_metrics = {
            'returnOnEquity' : "ROE_percentile",
            'FF_Quality_Growth' : "FFQ_growth_percentile",
            "FF_Quality_actual": "FFQ_actual_percentile"
            }

    for row in final_frame.index:
        for metric in inv_metrics.keys():
            final_frame.loc[row, inv_metrics[metric]] = 1-(stats.percentileofscore(final_frame[metric], final_frame.loc[row, metric])/100)
    
    return(final_frame)
    