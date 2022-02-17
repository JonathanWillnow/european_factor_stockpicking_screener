"""
Task file to execute the data scraping that is done as a first step

The following is done:
 - collect wkn and names of stocks on all different available indicies and exchnages listed on traderfox.de

The following is planned but is quite complicated to achieve because it is 1) really slow, 2) using a lot of selenium and is therefore prone to fail:
 - collect info on the stocks, such as industry, ISIN, ticker_de and ticker (This is sofar done manually by calling the script and let it run overnight)

"""

import numpy as np
import pytask

from src.config import SRC
from src.data_management.stockinfo_scraper import get_stock_data


# def save_data(sample, path):
#     sample.to_pickle(path)

# @pytask.mark.produces(SRC / "data_management" / "data" / "de_initial.pkl")
# def task_get_DEStocks(produces):
#     file = get_stock_data("https://traderfox.de/aktien/deutschland-160-bestandteile", "DE")
#     save_data(file, produces)

# @pytask.mark.produces(SRC / "data_management" / "data" / "eurostoxx600_initial.pkl")
# def task_get_EuroStoxx600Stocks(produces):
#     file = get_stock_data("https://traderfox.de/aktien/stoxx-europe-600-bestandteile", "EuroStoxx600")
#     save_data(file, produces)

# @pytask.mark.produces(SRC / "data_management" / "data" / "nyse_initial.pkl")
# def task_get_NYSEStocks(produces):
#     file = get_stock_data("https://traderfox.de/aktien/alle-nyse-aktien-bestandteile", "NYSE")
#     save_data(file, produces)

