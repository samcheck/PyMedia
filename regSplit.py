#!/usr/bin/python3
# regSplit.py -

import re, os

def Split(media_item):
    if not os.path.isfile(media_item):
        raise Exception('Not a file.')
    # Make TV regex, 2 groups all chars before Season/Ep and Season/Ep
    tv_regex = re.compile(r'(.*)([Ss]\d\d[Ee]\d\d)')
    # Make Movie regex, 2 groups all chars before (year) and (year)
    # seem to need to match an additional backslash in the regex based on being
    # passed a string literal
    movie_regex = re.compile(r'(.*)(\\?\(\d{4}\\?\))')

    # First attempt to match and exract movie
    media_match = movie_regex.search(os.path.basename(media_item))

    if media_match:
        title = media_match.group(1).replace('\\', '').strip()
        year = media_match.group(2).replace('\\', '').replace('(', '').replace(')', '').strip()
        return{'type': 'movie', 'title': title, 'year': year}

    # If no valid movie_regex is found, try tv_regex
    media_match = tv_regex.search(os.path.basename(media_item))

    # If neither match, raise exception as invalid formatted
    if media_match:
        title = media_match.group(1).replace('\\', '').strip()
        season = media_match.group(2).upper().split('E')[0].replace('S','')
        episode = media_match.group(2).upper().split('E')[1]
        return{'type': 'tv', 'title': title, 'season': season, 'episode': episode}
    else:
        raise Exception('Item not formatted as a Movie or TV show')

    # TODO: return as a dict 'title', 'Year' (if movie), 'Season' (if TV),
    # 'Episode' (if TV), type ('tv' or 'movie')
