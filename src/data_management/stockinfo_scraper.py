import urllib.request, json , time, os, difflib, itertools
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool
import datetime
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


def get_stock_data(url, index_exchange):
    """
    Function to fetch stock information from a specified URL of the traderfox.de website
    with an specified index / exchange

    Inputs:
        url (str): one of the available urls from traderfox.de
        index_exchange (str): name of the index / exchnage from which
            the stocks should be selected
    """
    browser =  webdriver.Firefox()
    time.sleep(2)
    browser.get(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source,"html")
    time.sleep(5)
    names = []
    Row = soup.find('table', attrs = {'id' : 'insert-stocks'})
    for name in Row.find_all('td', attrs = {'class' : 'name'}):
            try:
                names.append(name.text)
            except:
                names.append("")

    wkns = []
    Row = soup.find('table', attrs = {'id' : 'insert-stocks'})
    for wkn in Row.find_all('td', attrs = {'data-id' : 'wkn'}):
            try:
                wkns.append(wkn.text)
            except:
                wkns.append("")

    FRAME = pd.DataFrame.from_dict(
            {'name': names,
            'wkn': wkns,
            'index' : index_exchange
            })
    time.sleep(1)
    browser.quit()
    return(FRAME)


def get_ticker(initial_frame):
    url_ticker = "https://www.finanznachrichten.de/"
    url_yf_ticker = "https://finance.yahoo.com/quote/FB?p=FB"
    browser =  webdriver.Firefox()
    extension_path = r"C:\Users\Jonathan\AppData\Roaming\Mozilla\Firefox\Profiles\wl4weym2.default-1633941918487\extensions\jid1-MnnxcxisBPnSXQ@jetpack.xpi"
    browser.install_addon(extension_path, temporary=True)
    time.sleep(2)
    browser.get("about:support")
    time.sleep(5)
    browser.get(url_ticker)
    time.sleep(20)
    #clear = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[2]/button"))).click()
    time.sleep(1)
    ticker = []
    de_ticker = []
    industry = []
    ISIN = []
    for i, wkn in enumerate(initial_frame.wkn):
        print(len(de_ticker), len(industry), len(ISIN))
        # if wkn not valid
        if wkn == "-":
            de_ticker.append("not_found")
            industry.append("not_found")
            ISIN.append("not_found")
            continue
        try:
            clear = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fnk-suche-eingabe"))).clear()
            time.sleep(3)
            search = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fnk-suche-eingabe")))
            time.sleep(1)
            search.send_keys(str(wkn))
            time.sleep(4)
            browser.find_element_by_css_selector('#suchhilfeListe > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)').click()
            time.sleep(random.randint(3,5))
            de_ticker.append(str(WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#produkt-ticker"))).text.replace("Ticker-Symbol: ", "").lstrip()))
            #time.sleep(2)
        except:
            de_ticker.append("not_found")
            industry.append("not_found")
            ISIN.append("not_found")
            continue
        try:
            industry.append(str(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".a > a:nth-child(2)"))).text))
            time.sleep(1)
        except:
            industry.append("not_found")
        try:
            ISIN.append(str(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#produkt-isin"))).text.replace("ISIN: ", "").lstrip()))
            time.sleep(1)
            #time.sleep(random.randint(2,4))
        except:
            ISIN.append("not_found")


        if i % 4 == 0:
            try:
                browser.refresh()
                time.sleep(4)
            except:
                pass

    #check if lengths are equal   
    print(len(industry), len(ISIN), len(de_ticker))
    try:
        browser.get(url_yf_ticker)
        time.sleep(5)
    except:
        browser.get(url_yf_ticker)
        time.sleep(5)
    try:
        browser.find_element_by_css_selector("#scroll-down-btn").click()
        time.sleep(3)
    except:
        pass
    try:
        browser.find_element_by_css_selector("button.btn:nth-child(5)").click()
        time.sleep(4)
    except:
        pass
    for _ISIN in ISIN:
        if _ISIN == "not_found":
            ticker.append("not_found")
            continue
        time.sleep(2)
        #check again for popup and scroll
        try:
            browser.find_element_by_css_selector("#scroll-down-btn").click()
            time.sleep(3)
        except:
            pass
        try:
            browser.find_element_by_css_selector("button.btn:nth-child(5)").click()
            time.sleep(4)
        except:
            pass

        clear = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yfin-usr-qry"))).clear()
        #time.sleep(1)
        try:
            search = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#yfin-usr-qry")))
            #time.sleep(1)
            search.send_keys(str(_ISIN))
            time.sleep(2)
            ticker.append(str(WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#result-quotes-0 > div.modules_quoteLeftCol__gkCSv.modules_Ell__77DLP.modules_IbBox__2pmLe > div.modules_quoteSymbol__hpPcM.modules_Ell__77DLP.modules_IbBox__2pmLe"))).text))
        except:
            ticker.append("not_found")
            
    print(len(ticker))      

    frame = pd.DataFrame.from_dict(
        {"name" : initial_frame.name,
        "wkn" : initial_frame.wkn,
        "index" : "NASDAQ",
        'de_ticker' : de_ticker,
        'ticker': ticker,
        'industry': industry,
        'ISIN': ISIN
        })
    time.sleep(1)
    browser.quit()
    return frame