# european_factor_stockpicking_screener
This project provides an automatization of stockscreening of international stocks and helps the individualinvetor to construct her/his portfolio, based on common Asset-Pricing Factors.

I decided to deploy my results as an Dash-App on Heroku. This allows users to access my results and my research without having a proper background in programming and git.
Furthermore, I plan to publish it in a big german stockpicking / financial markets community called "Kleine Finanzzeitung", to contribute back to them. Therefore, I wanted to have a shiny application rather than a folder of .csv files :) 

#### Therefore, the final result can be seen here: https://stockpickingapp.herokuapp.com
The code that is used for this is the same as you can find in this repo in the folder src/Dashboard since I cannot publish the repository that is deployed on Heroku.
## Documentation
Since I was determined to deploy the project as a Dash-App, I decided to move the documentation on the web. This repo just contains a copy of this documentation as a latex file.
## Requirements
There are three files that list the requirements for this project:
- scraper_env.yml contains all requirements that are needed to use the scrapers.
- environment.yaml contains all reqquirements to build the output/product from the scraped data
- requirements.txt contains all requirements to run the DashApp alone

Updating the environment from environment.yml to try out the scraper can be done by:

`conda activate stockpicking_screener`

`conda env update --file sraper_env.yml --prune`

Since the requirements for the Dash-App are also contained in the environment.yml, I recommend to use the environment.yml file if you just want to have a look at the tasks and processes involved in the building of the final product. If you want to try the scraping, go ahead but keep in mind that it will take several hours/ days to scrape all the stocks and at least hours to scrape the corresponding metrics and numbers.

## Usage of pytask
Througggout the project I will make use of pytask. I even used pytask for scraping and showed that it works, but I also implemented all functionality in the form of scripts.
### Why didnt I used pytask more?
The longterm idea for this is that the project runs continously on a seperat machine and scrapes the stocks, for Instance every weekend at a fixed time. Therefore, I want to use the functionality of crontab, which is a demon on unix to start processes timely. Since I did not figure out how to use crontab together with pytask, I designed the project such that I can simply call the .py files. This is subject to change in the future since I more and more enjoy the possibilities that pytask provides.



