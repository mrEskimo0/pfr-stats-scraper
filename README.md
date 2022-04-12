# Pro Football Reference Stats Scrape

## Description

This is a set of python scripts that scrape pro football reference for all skilled position players' (QBs, WRs, RBs, TEs) biography information, draft information, and stats since the year 2000. The information scraped is committed to a MySQL database and is used for analytics by 3rd and 20.

## Draft Scraper

This script loops through all of the draft pages in pro football reference and scrapes all of the fantasy football eligible players and commits them to a MySQL database. 

## Stats Scraper

This script queries the database for all players acquired from the draft scraper, and scrapes the biography, year stats, and game logs for all players in the query. 

