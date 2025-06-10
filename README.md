# League of Legends Pro Stats
## Description
This is streamlit applicaton, which you can find [here](https://harry-capstone.streamlit.app/). It uses an ETL pipeline created using python to ingest data from the Riot API to collect, store, transform, and display statistics about league of legends professional players.
## Motivation
I decided to create this application to compare different league of legends pro players and see if there was any trends in the data. I could then look at the site to garner the player's opinion on what they believe to be the correct choices to make by which champions they choose to play and items they buy. I can then use this information to further inform my own choices when playing and hopefully increase my own skill and decision making in game.
## Usage
You can find the site [here](https://harry-capstone.streamlit.app/). Included in the repo is also the extraction script that I used. If you wish to use it to collect your own data for your own data base, check extraction script instructions.

# Extraction Script Instructions

## Setup
.env, ingestion.py, requirements.txt must be on the same level of the directory like so:\
![folder](./images/formating.png)


## First step:
### Create virtual environment

## Second step:
### Install the dependencies

pip install -r requirements.txt

## Third step:
### Run the script ingestion.py

python ingestion.py


# Chron Details

Every 2 hours
