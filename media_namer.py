#!/usr/bin/python3
# media_namer.py - Renames passed media files in a folder (and subfolders) using
#                   OMDB for movies and theTVDB for TV shows


import os
import sys
import logging
from distutils.util import strtobool

import tqdm

import videoLister
import scrapeOMDB
import scrapeTVDB
import regSplit

logger = logging.getLogger(__name__)
logging.basicConfig(filename='media_namer.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

in_path = ' '.join(sys.argv[1:])

JWT = scrapeTVDB.auth()

for item in tqdm.tqdm(videoLister.videoDir(in_path)):
    logger.info(("Working on: " + os.path.abspath(item)))
    reg_dict = regSplit.Split(item)
    ext = os.path.splitext(item)[1]

    if reg_dict['type'] == 'tv':
        med_info = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'], JWT)

        new_name = (reg_dict['title'] + ' S' + reg_dict['season'].zfill(2) +
                        'E' + reg_dict['episode'].zfill(2) + ' - ' +
                        med_info['data'][0]['episodeName'] + ext)

        logger.info("Renaming: %s, as: %s" % (item, new_name))
        os.rename(item, (os.path.join(os.path.dirname(item), new_name)))

    else:
        logger.warning(("File not renamed: "+ os.path.abspath(item)))

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])

        if strtobool(med_info['Response']):
            new_name = (reg_dict['title'] + ' (' + med_info['Year'] + ')' + ext)
            logger.info("Renaming: %s, as: %s" % (item, new_name))
            os.rename(item, (os.path.join(os.path.dirname(item), new_name)))
        else:
            logger.warning(("File not renamed: "+ os.path.abspath(item)))
