#!/usr/bin/python3
# scrapeOMDB.py - parses a movie and year from arguments and returns JSON

import json
import requests

URL_BASE = 'http://www.omdbapi.com/?'

def OMDBmovie(mTitle, mYear):
    """Gets movie info from omdbapi.com

    Arguments:
        mTitle: Title of the movie to match
        mYear: Year the movie was released

    Returns:
        theJSON: a dictionary with key value pairs matching return from OMDB

    """
    # Craft the URL
    url = URL_BASE + 't=' + mTitle + '&y=' + str(mYear) + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    theJSON = json.loads(response.text)
    return(theJSON)


def OMDBtv(tvTitle, tvSeason, tvEpisode):
    """Gets tv info from omdbapi.com

    Arguments:
        tvTitle: Title of the TV series to match
        tvSeason: Season number of the TV show
        tvEpisode: Episode number of the TV show

    Returns:
        theJSON: a dictionary with key value pairs matching return from OMDB

    """
    # Craft the URL
    url = URL_BASE + 't=' + tvTitle + '&Season=' + str(tvSeason) + '&Episode=' + str(tvEpisode) + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    theJSON = json.loads(response.text)
    return(theJSON)
