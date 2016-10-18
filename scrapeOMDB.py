#!/usr/bin/python3
# scrapeOMDB.py - parses a movie and year from arguments and returns JSON

import json, requests

URL_BASE = 'http://www.omdbapi.com/?'

def OMDBmovie(mTitle, mYear):
    # Craft the URL
    url = URL_BASE + 't=' + mTitle + '&y=' + mYear + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    theJSON = json.loads(response.text)
    return(theJSON)

def OMDBtv(tvTitle, tvSeason, tvEpisode):
    # Craft the URL
    url = URL_BASE + 't=' + tvTitle + '&Season=' + str(tvSeason) + '&Episode=' + str(tvEpisode) + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    theJSON = json.loads(response.text)
    return(theJSON)
