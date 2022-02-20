from unicodedata import name
import urllib.request, json , time, os, difflib, itertools
from datetime import datetime
import time
import numpy as np
import pandas as pd
from scipy import stats #The SciPy stats module
from multiprocessing.pool import ThreadPool
import pytask
from src.config import SRC
#from src.data_management.stockinfo_scraper import get_stock_data



def get_data(stockticker):
    stock = None

    metrics_list = ['enterpriseValue', "marketCap",'forwardPE', "trailingPE", 'profitMargins', 'floatShares', "sharesOutstanding", 
                    'priceToBook', 'heldPercentInsiders', 'bookValue', 'priceToSalesTrailing12Months', 'trailingEps', 'forwardEps',
                    'pegRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', "dividendYield"]

    financial_list = ["currentPrice","quickRatio","currentRatio", "debtToEquity", "returnOnAssets", "returnOnEquity",
                    "revenueGrowth", "grossMargins", "ebitdaMargins", "operatingMargins", "profitMargins"]# "PB_percentile", "EV_percentile", "PS_percentile"]

    check_list = ['forwardPE', "trailingPE", "marketCap", 'priceToSalesTrailing12Months', "dividendYield"]

    #get exchange
    #countrycode = stockinfo.ISIN[stockinfo.ticker == stockticker].values[0][:2]
   
    stock = str(stockticker) #+ ".F"
    print(stock)
    data_dict = {}
    data_dict["ticker"] = stock
    data_dict["date"] = datetime.today().strftime("%Y-%m-%d")
    try:
        query_url_1= "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=defaultKeyStatistics"

        with urllib.request.urlopen(query_url_1) as url:
                    parsed_1 = json.loads(url.read().decode())
        data_dict["industry"] = stockinfo_pkl.industry[stockinfo_pkl.ticker == stockticker].values[0]
        data_dict["de_ticker"] = stockinfo_pkl.de_ticker[stockinfo_pkl.ticker == stockticker].values[0]
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
        
        try:
            query_url_3 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=summaryDetail"
            with urllib.request.urlopen(query_url_3) as url:
                    parsed_3 = json.loads(url.read().decode())
            data_dict[metric] = parsed_3["quoteSummary"]["result"][0]["summaryDetail"][metric]["raw"]
        except:
            pass
    
    ## FF Quality
    FF_Quality_year_frame = calculate_FF_Quality(stock)
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

    
    # FF_Conservative
    FF_Conservative_year_frame = calculate_FF_CA(stock)
    try:
        data_dict["FF_Assets_Growth_mean"] = FF_Conservative_year_frame.sort_values(["year"], ascending=False)[["totalAssets"]].pct_change().mean()[0]
        data_dict["FF_Assets_Growth_actual"] = FF_Conservative_year_frame.sort_values(["year"], ascending=False)[["totalAssets"]].pct_change().iloc[1,0]
    except:
        data_dict["FF_Assets_Growth_mean"] = np.nan
        data_dict["FF_Assets_Growth_actual"] = np.nan


    frame = pd.DataFrame.from_dict({stock : data_dict}, orient="index")

    return(frame)

def calculate_FF_Quality(stock): 

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
        print(stock)

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
    return(FF_Quality_year_frame)


def calculate_FF_CA(stock): 

    FF_Conservative_dict = {}
    FF_Conservative_year_frame = pd.DataFrame({})
    try:
        query_url_5 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+str(stock)+"?modules=balanceSheetHistory"
        with urllib.request.urlopen(query_url_5) as url:
                    parsed_5 = json.loads(url.read().decode())
    except Exception as e:
        print(e)
        print(stock)

    # FF Inv
    for year in range(0,10):
        try:
            FF_Conservative_dict["totalAssets"] = parsed_5["quoteSummary"]["result"][0]["balanceSheetHistory"]["balanceSheetStatements"][year]["totalAssets"]["raw"]
            FF_Conservative_dict["year"] = year 
            FF_Conservative_frame = pd.DataFrame.from_dict({stock : FF_Conservative_dict}, orient="index")
            FF_Conservative_year_frame = FF_Conservative_year_frame.append(FF_Conservative_frame)
        except:
            break
    return(FF_Conservative_year_frame)


def calc_precentiles(final_frame):

    metrics = {
            'priceToBook':'PB_percentile',
            'enterpriseValue': 'EV_percentile',
            'marketCap': 'MC_percentile',
            'priceToSalesTrailing12Months' : 'PS_percentile',
            'enterpriseToRevenue' : "EToRev_precentile",
            'enterpriseToEbitda' : "EToEbitda_percentile",
            "FF_Assets_Growth_mean" : 'FFA_m_percentile',
            "FF_Assets_Growth_actual" : "FF_Cons_actual_percentile",
            }
    for row in final_frame.index:
        for metric in metrics.keys():
            try:
                final_frame.loc[row, metrics[metric]] = stats.percentileofscore(final_frame[metric], final_frame.loc[row, metric])/100
            except: 
                final_frame.loc[row, metrics[metric]] = np.nan

    # metrics where we have to invert the percentile
    inv_metrics = {
            'returnOnEquity' : "ROE(inv)_percentile",
            'FF_Quality_Growth' : "FFQ(inv)_g_percentile",
            "FF_Quality_actual": "FFQ(inv)_a_percentile",
            'FF_Quality_mean' : 'FFQ(inv)_m_percentile',
            }

    for row in final_frame.index:
        for metric in inv_metrics.keys():
            try:
                final_frame.loc[row, inv_metrics[metric]] = 1-(stats.percentileofscore(final_frame[metric], final_frame.loc[row, metric])/100)
            except:
                final_frame.loc[row, inv_metrics[metric]] = np.nan
    
    return(final_frame)



def clean_stock_selection(stocks):
    return(stocks[stocks.industry != "not_found"])
    #return(clean_stocks[clean.industry != "Finanzdienstleistungen"])

def save_data(sample, path):
    sample.to_pickle(path)


stockinfo_pkl_task = pd.read_pickle( SRC / "data_management" / "data" / "val2_euro600.pkl")
today = datetime.today().strftime("%Y-%m-%d")
@pytask.mark.produces(SRC / "data_management" / f"proc_eurostoxx600_{today}.pkl")
def task_process_eu_stocks(produces):

    stockinfo_pkl = pd.read_pickle( SRC / "data_management" / "data" / "val_eurostoxx600_stocks.pkl")   
    stocklist =  clean_stock_selection(stockinfo_pkl_task)
    frame = pd.DataFrame({})
    with ThreadPool() as p:
        frame = frame.append(p.map(get_data , stocklist.ticker[1:5]))
        p.close()
    final_frame = calc_precentiles(frame)
    save_data(final_frame, produces)


def fun_process_stocks(stockinfo_pkl, datalist):

    stocklist =  clean_stock_selection(stockinfo_pkl)
    try:
        stocklist.drop('Unnamed: 0', axis=1, inplace=True)
    except:
        pass
    frame = pd.DataFrame({})
    with ThreadPool() as p:
        frame = frame.append(p.map(get_data, stocklist.ticker))
        p.close()
    final_frame = calc_precentiles(frame)
    save_data(final_frame, SRC / "data_management" / "processed_data" / f"proc_{today}_{datalist}")

import warnings
warnings.filterwarnings("ignore")
if __name__ == "__main__":
    
    today = datetime.today().strftime("%Y-%m-%d")
    data_ls = ["val2_de.pkl",
               "val2_euro600.pkl",
               "val2_nyse.pkl",
               "val2_nasdaq.pkl",
               "val2_nikkei225.pkl",
               "val2_amex.pkl"]
    for datalist in data_ls:
        stockinfo_pkl = pd.read_pickle( SRC / "data_management" / "data" / datalist)  
        fun_process_stocks(stockinfo_pkl, datalist)
        time.sleep(1)
