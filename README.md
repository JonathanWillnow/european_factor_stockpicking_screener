# european_factor_stockpicking_screener
This project provides an automatization of stockscreening of international stocks and helps the individualinvetor to construct her/his portfolio, based on common Asset-Pricing Factors.

I decided to deploy my results as an Dash-App on Heroku. This allows users to access my results and my research without having a proper background in programming and git.
Furthermore, I plan to publish it in a big german stockpicking / financial markets community called "Kleine Finanzzeitung", to contribute back to them. Therefore, I wanted to have a shiny application rather than a folder of .csv files :) 

#### Therefore, the final result can be seen here: https://stockpickingapp.herokuapp.com
The code that is used for this is the same as you can find in this repo in the folder src/Dashboard since I cannot publish the repository that is deployed on Heroku. You can therefore also locally run the Dash-App, but you can also just check it out at https://stockpickingapp.herokuapp.com.
## Documentation and Idea
Since I was determined to deploy the project as a Dash-App, I decided to move part of it on the web. This repo just contains the documentation of the functions, while the motivation and idea behind this project can be found at https://stockpickingapp.herokuapp.com/documentation, but also partly in the research paper of this project.
## Requirements
There are three files that list the requirements for this project:
- scraper_env.yml contains all requirements that are needed to use the scrapers.
- environment.yaml contains all reqquirements to build the output/product from the scraped data
- requirements.txt contains all requirements to run the DashApp alone

Example: Updating the environment from environment.yml to try out the scraper can be done by:

`conda activate stockpicking_screener`

`conda env update --file sraper_env.yml --prune`

Since the requirements for the Dash-App are also contained in the environment.yml, I recommend to use the environment.yml file if you just want to have a look at the tasks and processes involved in the building of the final product. If you want to try the scraping, go ahead but keep in mind that it will take several hours/ days to scrape all the stocks and at least hours to scrape the corresponding metrics and numbers.

## Usage of pytask
Througggout the project I will make use of pytask. I even used pytask for scraping and showed that it works, but I also implemented all functionality in the form of scripts.
### Why didnt I used pytask more?
The longterm idea for this is that the project runs continously on a seperat machine and scrapes the stocks, for instance every weekend or every two weeks at a fixed time. Therefore, I want to use the functionality of crontab, which is a demon on unix to start processes timely. Since I did not figure out how to use crontab together with pytask, I designed the project such that I can simply call the .py files. This is subject to change in the future since I more and more enjoy the possibilities that pytask provides.

## Work in progress
This project is not finished and work in progress. After I started it for the course Effective Programming Practices for Economists, I became aware of all the possible extensions that I could develop and implement. As outlined in the beginning, I want to make it Open Source and find contributers after the grading for EPP is done



