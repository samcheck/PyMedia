#!/usr/bin/python3
# scrapeOMDB.py - parses a movie and year from arguments and returns JSON

import requests

URL_BASE = 'http://www.omdbapi.com/?'

def OMDBmovie(mTitle, mYear):
    """Gets movie info from omdbapi.com

    Arguments:
        mTitle: Title of the movie to match
        mYear: Year the movie was released

    Returns:
        a dictionary with key value pairs matching return from OMDB

    """
    # Craft the URL (with full plot and json response)
    url = URL_BASE + 't=' + mTitle + '&y=' + str(mYear) + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    return(response.json())


def OMDBtv(tvTitle, tvSeason, tvEpisode):
    """Gets tv info from omdbapi.com

    Arguments:
        tvTitle: Title of the TV series to match
        tvSeason: Season number of the TV show
        tvEpisode: Episode number of the TV show

    Returns:
        a dictionary with key value pairs matching return from OMDB

    """
    # Craft the URL (with full plot and json response)
    url = URL_BASE + 't=' + tvTitle + '&Season=' + str(tvSeason) + '&Episode=' + str(tvEpisode) + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    return(response.json())


def OMDBid(IMDB_id):
    """Gets media info from omdbapi.com

    Arguments:
        IMDB_id: IMDB id of media to match

    Returns:
        a dictionary with key value pairs matching return from OMDB

    """
    # Craft the URL (with full plot and json response)
    url = URL_BASE + 'i=' + IMDB_id + '&plot=full&r=json'

    # Try to get the url
    response = requests.get(url)
    response.raise_for_status()

    return(response.json())
