"""
TBD

"""

import itertools
import numpy as np
import pytask

from src.config import BLD
from src.config import SRC
from src.final.product import *
from datetime import datetime

def save_data(sample, path):
    sample.to_csv(path, encoding = 'utf-8')


today = datetime.today().strftime("%Y-%m-%d")

@pytask.mark.produces(SRC / "product_data" / f"NYSE_product.csv{today}")
def task_create_product(produces):
        
    rv_dataframe = pd.read_csv(r"src\final\processed_NYSEStocks_2022-02-01.csv")
    rv_dataframe.drop('Unnamed: 0', axis=1, inplace=True)

    rv_dataframe_per = calculate_precentiles(rv_dataframe)
    rv_dataframe_revGPconstraint = rv_dataframe_per[(rv_dataframe_per.RevGrowth >= 0.07) & (rv_dataframe_per.GrossProfitGrowth >= 0.075) & (rv_dataframe_per.returnOnEquity >= 0) & (rv_dataframe_per.OpIncomeGrowth >= 0.05)]
    len(rv_dataframe_revGPconstraint)

    sorted_rc_frame = rv_dataframe_revGPconstraint.sort_values(by = 'RV Score').copy()
    sorted_rc_frame  = sorted_rc_frame
    sorted_rc_frame .reset_index(drop = True, inplace = True)
    sorted_rc_frame[['ticker', 'industry','RV Score','priceToBook', 'heldPercentInsiders','returnOnAssets', 'returnOnEquity', 'RevGrowth',
        'GrossProfitGrowth', 'OpIncomeGrowth','PB_percentile','MC_percentile', 'FFA_m_percentile','FFQ(inv)_a_percentile']]
#sorted_rc_frame.columns


    save_data(sorted_rc_frame, produces)

