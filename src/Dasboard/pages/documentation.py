from dash import dcc, html, Input, Output, callback

layout = html.Div(
    children=[
        html.H1(children="Documentation", className="header-title"),
        html.P(
            children=[
                "This is the final project for the course Effective Programming Practices for Economists"
                + " by Prof. Gaudecker in the winterterm 21/22 of the University of Bonn by Jonathan Willnow. \n"
                + "The project repository is avaialble ",
                html.A(
                    "on Github",
                    href="https://github.com/JonathanWillnow/european_factor_stockpicking_screener",
                ),
            ],
            className="justified",
        ),
        html.P(
            children=[
                html.H5(children="Purpose", className="header-title-2"),
                html.P(
                    children="In recent years, there was a rising interest in investing and personal fincance"
                    + "for indiviudal private investors. While this was especially driven and pronounced in the"
                    + "recovery of the covid-19 crash and fueled by pressumed easy gains, reddit boards,"
                    + " meme stocks and false assumptions, a whole new generation of investors entered the"
                    + "capital markets. While for the majority of private investors it holds true that they"
                    + "should invest in an index fund, this project tries to provide an easy, scientific proofen"
                    + " concept towards stock picking and the managing of our own finances using factor investing.",
                    className="justified",
                ),
                html.H5(children="Idea and Methodology", className="header-title-2"),
                html.P(
                    children=[
                        "The idea apperas simple: There exist more than only one risk factor ___ that determines the"
                        + "performance of a portfolio (here, portfolio is assumed to be a index/ market portfolio)."
                        + " Fama and French came up with the Fama and French three factor model tah includes"
                        + " the size of firms, their book-to-market values, and their excess return on the market. In other words, "
                        + "the three factors used are SMB (small minus big), HML (high minus low), and the "
                        + "market return return less the risk-free rate of return. Building up on their work, many other"
                        + "factors have been researched and found like the Fama French Quality Factor and Conservative "
                        + "Asset factor or the Carhartd Momentum Factor. While the Momentum Factor finds strong "
                        + "empirical support like the other factors, this project sofar is limited to the factors "
                        + "found by Fama and French. \n\n"
                        + "A selection of individual Stocks is available for Europe, Germany, Japan and North America"
                        + "that was collected using several scrapers and validation mehtods. To obtain reliable metrics"
                        + f",the metrics are collected from ",
                        html.A("Yahoo Finance", href="https://finance.yahoo.com"),
                        " using the functionality of the python packe urllib.requests. The so obtained metrics were then "
                        + "used to compute the introduced factors according to the work of Fama and French. To present the "
                        + "results and allow for easy filtering, I decided to deploy this simple Dash App.",
                    ],
                    className="justified",
                ),
            ]
        ),
    ]
)
