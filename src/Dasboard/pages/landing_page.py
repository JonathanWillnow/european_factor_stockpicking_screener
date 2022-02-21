from dash import dcc, html, Input, Output, callback

layout =  html.Div(
    children=[
        html.H1(children="Factor Stockscreener",
        className="header-title"),
        html.P(
            children="Analyze your favorite stocks with different Asset-Pricing-Factors, compare them to their peers",
            className="header-description",
        )
        ]
    )
       
