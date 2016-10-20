#!/usr/bin/python3
# regSplit.py - Use regex to split up the media file and return a dict

import re
import os


def Split(media_item):
    """Splits the media file's name using regex.

    Splits a filename into title and year if movie and title,
    season and episode if TV.

    Argument:
    media_item: a media file (full path and basename).

    Returns:
        A dictionary maping keys to extracted file info, each key maps to a
        single string. For example:

        {'type': 'movie',
        'title': 'Finding Nemo',
        'year': 2003}

        Raises:
            Exception: Not a file.
            Exception: Item not formatted as a Movie or TV show.
    """
    # Test if the parameter is a valid file
    if not os.path.isfile(media_item):
        raise Exception('Not a file.')

    # Make TV regex, 2 groups [all chars before Season/Ep] and [Season/Ep]
    tv_regex = re.compile(r'(.*)([Ss]\d\d[Ee]\d\d)')

    # Make movie regex, 2 groups [all chars before (year)] and [(year)]
    # seem to need to optionally match an additional backslash in the regex
    # based on being passed a string literal
    movie_regex = re.compile(r'(.*)(\\?\(\d{4}\\?\))')

    # First attempt to match and extract movie
    media_match = movie_regex.search(os.path.basename(media_item))

    if media_match:
        # Clean up title and year
        title = media_match.group(1).replace('\\', '').replace('.', ' ').strip().title()
        year = media_match.group(2).replace('\\', '').replace('(', '').replace(')', '').strip()

        # Return a dict w/ 'title', 'year' (movie), type ('tv' or 'movie')
        return{'type': 'movie', 'title': title, 'year': year}

    # If no valid movie_regex is found, try tv_regex
    media_match = tv_regex.search(os.path.basename(media_item))

    if media_match:
        # Clean title and split season and episode
        title = media_match.group(1).replace('\\', '').replace('.', ' ').strip().title()
        season = media_match.group(2).upper().split('E')[0].replace('S','')
        episode = media_match.group(2).upper().split('E')[1]

        # Return a dict w/ 'title', 'season' (TV), 'episode' (TV), type ('tv' or 'movie')
        return{'type': 'tv', 'title': title, 'season': season, 'episode': episode}

    else:
        # If neither matches throw an exception that the file is not properly formatted
        raise Exception('Item not formatted as a Movie or TV show.')
