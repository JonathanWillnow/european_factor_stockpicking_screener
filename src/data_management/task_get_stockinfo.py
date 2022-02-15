"""
Task file to execute the data scraping that is done as a first step

The following is done:
 - collect wkn and names of stocks on all different available indicies and exchnages listed on traderfox.de

The following is planned but is quite complicated to achieve because it is 1) really slow, 2) using a lot of selenium and is therefore prone to fail:
 - collect info on the stocks, such as industry, ISIN, ticker_de and ticker (This is sofar done manually by calling the script and let it run overnight)

"""

import numpy as np
import pytask

from src.config import BLD
from src.config import SRC
from src.data_management.stockinfo_scraper import get_stock_data


def save_data(sample, path):
    sample.to_csv(path, encoding = 'utf-8')

url = "https://traderfox.de/aktien/alle-nasdaq-aktien-bestandteile"
index_exchange = "DE"

@pytask.mark.produces(BLD / "data" / "DEStocks.csv")
def task_get_simulation_draws(produces):
    file = get_stock_data(url, index_exchange)
    save_data(file, produces)
