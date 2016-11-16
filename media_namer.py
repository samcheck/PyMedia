#!/usr/bin/python3
# media_namer.py - Renames passed media files


import os
import sys
import logging
from distutils.util import strtobool

import tqdm

import videoLister
import scrapeOMDB
import regSplit

logger = logging.getLogger(__name__)
logging.basicConfig(filename='media_namer.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

in_path = ' '.join(sys.argv[1:])

for item in tqdm.tqdm(videoLister.videoDir(in_path)):
    reg_dict = regSplit.Split(item)
    ext = os.path.splitext(item)[1]

    if reg_dict['type'] == 'tv':
        med_info = scrapeOMDB.OMDBtv(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'])

        if strtobool(med_info['Response']):
            new_name = (reg_dict['title'] + ' S' + med_info['Season'].zfill(2) +
                        'E' + med_info['Episode'].zfill(2) + ' - ' +
                        med_info['Title'] + ext)
            logger.info("Renaming: %s, as: %s" % (item, new_name))
            os.rename(item, (os.path.join(os.path.dirname(item), new_name)))
        else:
            logger.warning(("File not renamed: "+ os.path.abspath(item)))

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])

        if strtobool(med_info['Response']):
            new_name = (reg_dict['title'] + '(' + med_info['Year'] + ')' + ext)
            logger.info("Renaming: %s, as: %s" % (item, new_name))
            os.rename(item, (os.path.join(os.path.dirname(item), new_name)))
        else:
            logger.warning(("File not renamed: "+ os.path.abspath(item)))
