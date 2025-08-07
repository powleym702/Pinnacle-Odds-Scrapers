# Pinnacle-Odds-Scrapers

## Overview

These scripts are meant to scrape pinnacle.com for player props that can be utilized to find value on pick-em websites such as PrizePicks, Underdog, Dabble, and more. The idea is to find props that are +EV and to find discrepancies in the market between a sharp site and a pick-em app. 

There is one script for each of the big 4 American sports leagues: MLB, NFL, NBA, and NHL. 

When ran, the script will output the props in the following format:

Justin Verlander,Under 2.5,Earned Runs,-142.0

Max Fried,Over 1.5,Earned Runs,-155.0

Michael Soroka,Over 1.5,Earned Runs,-138.0

## Functionality
First, the script uses Chromedriver to manually open the general pinnacle site for that league. It scrapes the current upcoming games to be played (not including live games), and then proceeds to each unique game url's player props page and scrapes for props with odds in the range -137 to -155. When using a taking vig into consideration, -137 is approximately the cutoff where props begin to be profitable, assuming the user is betting the highest EV lineup types. The range is capped at -155 since it is very rare that pick-em sites will leave a line up that is more skewed than that. 
