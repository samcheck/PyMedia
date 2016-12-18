#!/usr/bin/python3
# regSplit.py - Use regex to split up the media file and return a dict

import re
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='regSplit.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def Split(media_item):
    """Splits the media file's name using regex.

    Splits a filename into title and year if movie and title, season and episode
    if TV. The function expects a format of 'Series Title' '(S|s)(##|#)(E|e)(##|#)'
    or 'Movie Title' '(|[Year]|)'

    Argument:
    media_item: a media file (full path and basename).

    Returns:
        A dictionary maping keys to extracted file info, each key maps to a
        single string. For example:

        {'type': 'movie',
        'title': 'Finding Nemo',
        'year': 2003}

        if item is not formatted as a Movie or TV show (based on regex) return:

        {'type': None}
    """
    # Test if the parameter is a valid file, log a warning
    if not os.path.isfile(media_item):
        logger.warning('Not a file: %s' % media_item)

    # Make TV regex, 2 groups [all chars before Season/Ep] and [Season/Ep]
    # Optionally 1 or 2 numbers for season/episode
    tv_regex = re.compile(r'(.*)(([Ss]\d?\d[Ee]\d?\d)|(\d?\d[Xx]\d?\d))')

    # Make movie regex, 2 groups [all chars before (year)] and [(year)]
    # seem to need to optionally match an additional backslash in the regex
    # based on being passed a string literal
    movie_regex = re.compile(r'(.*)(\\?(\(|\[)\d{4}\\?(\)|\]))')

    # First attempt to match and extract movie
    media_match = movie_regex.search(os.path.basename(media_item))

    if media_match:
        logger.info('Matched movie format')
        # Clean up title and year
        title = media_match.group(1).replace('\\', '').replace('.', ' ').strip().title()
        year = media_match.group(2).replace('\\', '').replace('(', '').replace(')', '').strip()
        logger.info('Movie: %s (%s)' % (title, year))

        # Return a dict w/ 'title', 'year' (movie), type ('tv' or 'movie')
        return{'type': 'movie', 'title': title, 'year': year}

    # If no valid movie_regex is found, try tv_regex
    media_match = tv_regex.search(os.path.basename(media_item))

    if media_match:
        logger.info('Matched TV format')
        # Clean title and split season and episode
        title = media_match.group(1).replace('\\', '').replace('.', ' ').replace('-', ' ').strip().title()
        if len(media_match.group(2).upper().split('E')) == 2:
            season = media_match.group(2).upper().split('E')[0].replace('S','')
            episode = media_match.group(2).upper().split('E')[1]
        elif len(media_match.group(2).upper().split('X')) == 2:
            season = media_match.group(2).upper().split('X')[0]
            episode = media_match.group(2).upper().split('X')[1]
        else:
            logger.warning('Error splitting season and episode')
            return{'type': None}

        logger.info('TV: %s S%sE%s' % (title, season, episode))

        # Return a dict w/ 'title', 'season' (TV), 'episode' (TV), type ('tv' or 'movie')
        return{'type': 'tv', 'title': title, 'season': season, 'episode': episode}

    else:
        # If neither matches log a warning that the file is not properly
        # formatted and return a type None
        logger.warning('Item not formatted as a Movie or TV show.')
        return{'type': None}
