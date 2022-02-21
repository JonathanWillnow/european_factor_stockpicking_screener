import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from src.config import SRC

data_input_eu = pd.read_pickle(SRC / "final" / "processed_data" / "f_proc_2022-02-19_val2_euro600.pkl")

#data = data2[["ticker", "marketCap", "forwardPE",  "EV_percentile", "FFQ(inv)_a_percentile", "trailingPE","profitMargins","floatShares"]]
data = round(data_input_eu, 3)
data.sort_values("ticker", inplace=True)


layout = html.Div(
    children=[
        html.H1(children="European Stocks",
        className="header-title"),
        html.P(
            children="Browse through the european Stocks",
            className="header-description",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["ticker"],
                        "y": data["marketCap"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["ticker"],
                        "y": data["forwardPE"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            },
        ),
         html.Div(
            dash.dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(data.columns)
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
        html.H3(children="Avocado Analytics",
        style={'textAlign': 'center'}),
        html.Div(
            id='table-paging-with-graph-container',
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
    Output('table-paging-with-graph', "data"),
    Input('table-paging-with-graph', "page_current"),
    Input('table-paging-with-graph', "page_size"),
    Input('table-paging-with-graph', "sort_by"),
    Input('table-paging-with-graph', "filter_query"))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = data
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
    Output('table-paging-with-graph-container', "children"),
    Input('table-paging-with-graph', "data"))
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

