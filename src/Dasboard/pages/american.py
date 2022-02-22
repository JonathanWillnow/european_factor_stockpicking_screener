import dash
from dash import dcc, html
import pandas as pd
import json
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from src.config import SRC

import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns


data_input_america_1 = pd.read_pickle(SRC / "final" / "processed_data" / "f_proc_2022-02-19_val2_nyse.pkl")
data_input_america_2 = pd.read_pickle(SRC / "final" / "processed_data" / "f_proc_2022-02-19_val2_nasdaq.pkl")
data_input_america_3 = pd.read_pickle(SRC / "final" / "processed_data" / "f_proc_2022-02-19_val2_amex.pkl")

data_american_ = round(pd.concat([data_input_america_1, data_input_america_2, data_input_america_3]), 3)
data_american = data_american_.dropna(subset= ["MC_percentile", "PB_percentile","FFA_m_percentile", "FFQ(inv)_a_percentile"])
#data = data2[["ticker", "marketCap", "forwardPE",  "EV_percentile", "FFQ(inv)_a_percentile", "trailingPE","profitMargins","floatShares"]]

data_american.sort_values("ticker", inplace=True)

layout = html.Div(
    children=[
        html.H1(children="American Stocks",
        className="header-title"),
        html.P(
            children="Browse through the american stocks, selected from AMEX, NYSE and NASDAQ",
            className="header-description",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data_american["ticker"],
                        "y": data_american["marketCap"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        html.Div(id='click-data-123', style={'whiteSpace': 'pre-wrap'}
        ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data_american["ticker"],
        #                 "y": data_american["forwardPE"],
        #                 "type": "lines",
        #             },
        #         ],
        #         "layout": {"title": "Avocados Sold"},
        #     },
        # ),
         html.Div(
            dash.dash_table.DataTable(
                id='table-paging-with-graph-american',
                columns=[
                    {"name": i, "id": i} for i in sorted(data_american.columns)
                ],
                page_current=0,
                page_size=20,
                page_action='custom',

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
            ),
            style={'height': 700,
                   'overflowY': 'scroll',
                   'overflowX': 'scroll'},
           # className='six columns'
        ),
        html.H3(children="Further Analysis on selected metrics",
        style={'textAlign': 'center'}),
        html.Div(
            id='table-paging-with-graph-container-american',
            className="five columns",

            style={"margin-top": "25px"},
        ),
        ]
    )
        
    

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@dash.callback(
    Output('table-paging-with-graph-american', "data"),
    Input('table-paging-with-graph-american', "page_current"),
    Input('table-paging-with-graph-american', "page_size"),
    Input('table-paging-with-graph-american', "sort_by"),
    Input('table-paging-with-graph-american', "filter_query"))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = data_american
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@dash.callback(
    Output('table-paging-with-graph-container-american', "children"),
    Input('table-paging-with-graph-american', "data"))
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["ticker"],
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 350,
                        'title': column,
                        "margin": {"t": 35, "l": 10, "r": 10},
                    },
                },
                
            )
            for column in ["marketCap", "forwardPE",  "EV_percentile", "FFQ(inv)_a_percentile"]
        ]
    )

# define callback        
@dash.callback(
    Output('click-data-123', 'children'),
    [Input('table-paging-with-graph-american', 'active_cell')],
     # (A) pass table as data input to get current value from active cell "coordinates"
    [State('table-paging-with-graph-american', 'data')]
)
def display_click_data(active_cell, table_data):
    if active_cell:
        cell = json.dumps(active_cell, indent=2)    
        row = active_cell['row']
        col = active_cell['column_id']
        value = table_data[row]["ticker"]
        #out = '%s\n%s' % (cell, value)
    else:
        return
        #out = 'no cell selected'
    dff = get_data_d(value)
    return html.Div(
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x":dff.index,
                            "y": dff["adj_close"],
                            "type": "lines",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 400,
                        "title": f"Chart for {value}",
                        "margin": {"t": 35, "l": 10, "r": 10},
                    },
                },
                
            ))

def realized_volatility(x):
    return np.sqrt(np.sum(x**2))
    
def get_data_d(TICKR):
    df_yahoo = yf.download(TICKR,
    start='2000-01-01',
    end='2021-12-31',
    progress=False)
    df = df_yahoo.loc[:, ['Adj Close']]
    df.rename(columns={'Adj Close':'adj_close'}, inplace=True)
    df['simple_rtn'] = df.adj_close.pct_change()
    df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))
    return df

def get_data_m(TICKR):
    df_yahoo = yf.download(TICKR,
    start='2000-01-01',
    end='2020-12-31',
    progress=False)
    df = df_yahoo.loc[:, ['Adj Close']]
    df.rename(columns={'Adj Close':'adj_close'}, inplace=True)
    pd.to_datetime(df.index)
    df_mm = df.resample('1M').mean()
    df_mm['simple_rtn'] = df.adj_close.pct_change()
    df_mm['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))
    return df_mm

def indentify_outliers(row, n_sigmas=3):
    x = row['simple_rtn']
    mu = row['mean']
    sigma = row['std']
    if (x > mu + 3 * sigma) | (x < mu - 3 * sigma):
        return 1
    else:
        return 0


START_DATE = '2019-01-01'
END_DATE = '2020-12-31'

from pandas_datareader.famafrench import get_available_datasets
import pandas_datareader.data as web
import pandas as pd
ff_dict = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start=START_DATE, end = END_DATE) # default is monthly  #ff_dict.keys()  #print(ff_dict["DESCR"])
factor_df = ff_dict[0]#monthly factors. 1 for annual
factor_df.rename(columns = {"Mkt-RF": "mkt_rf", "SMB":"smb", "HML":"hml", "RF":"rf"}, inplace= True) 
factor_df["mkt"] = factor_df.mkt_rf + factor_df.rf
factor_df = factor_df.apply(pd.to_numeric, errors='coerce').div(100)

# Some stuff to play arroudn for now
