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


rv_dataframe = pd.read_csv(r"frameResults.csv")


def weighted_average_m1(distribution, weights):
  
    numerator = sum([distribution[i]*weights[i] for i in range(len(distribution))])
    denominator = sum(weights)
    
    return round(numerator/denominator,2)


from statistics import mean
metrics = {
        'priceToBook':'PB_percentile',
        'enterpriseValue': 'EV_percentile',
        'priceToSalesTrailing12Months' : 'PS_percentile'
        }
weights = [100,1,1]
for row in rv_dataframe.index:
    value_percentiles = []
    for i, metric in enumerate(metrics.keys()):
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]] * weights[i])
        #sum([distribution[i]*weights[i] for i in range(len(distribution))]) list comprehension
    rv_dataframe.loc[row, 'RV Score'] = sum(value_percentiles) / sum(weights)
    
rv_dataframe


sorted_rc_frame = rv_dataframe.sort_values(by = 'RV Score').copy()
sorted_rc_frame  = sorted_rc_frame [:25]
sorted_rc_frame.reset_index(drop = True, inplace = True)

position_size = float(1_000_000) / len(sorted_rc_frame.index)
for i in range(0, len(sorted_rc_frame['Unnamed: 0'])-1):
    sorted_rc_frame.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / sorted_rc_frame['currentPrice'][i])
sorted_rc_frame