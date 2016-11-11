#!/usr/bin/python3
# tv_namer.py - Renames passed media files of TV shows

import shutil
import os
import sys
import logging

import videoLister
import scrapeTVDB
import regSplit

logger = logging.getLogger(__name__)
logging.basicConfig(filename='tv_namer.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


in_path = ' '.join(sys.argv[1:])

for item in videoLister.videoDir(in_path):
    logger.info("Working on: ", item)
    reg_dict = regSplit.Split(item)
    ext = os.path.splitext(item)[1]

    if reg_dict['type'] == 'tv':
        med_info = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'])

        new_name = (reg_dict['title'] + ' S' + reg_dict['season'].zfill(2) +
                        'E' + reg_dict['episode'].zfill(2) + ' - ' +
                        med_info['data'][0]['episodeName'] + ext)

        logger.info("Renaming: %s, as: %s" % (item, new_name))
        shutil.move(item, (os.path.join(os.path.dirname(item), new_name)))

    else:
        logger.info("File not renamed: ", item)
