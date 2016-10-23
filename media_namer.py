#!/usr/bin/python3
# media_namer.py - Renames passed media files

import shutil
import os
import sys
import tqdm
from distutils.util import strtobool
import videoLister
import scrapeOMDB
import regSplit

in_path = ' '.join(sys.argv[1:])

media_list = videoLister.videoDir(in_path)
files_no_response = []
for item in tqdm.tqdm(media_list):
    med_info = {}
    reg_dict = regSplit.Split(item)
    ext = os.path.splitext(item)[1]

    if reg_dict['type'] == 'tv':
        med_info = scrapeOMDB.OMDBtv(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'])

        if strtobool(med_info['Response']):
            new_name = (reg_dict['title'] + ' S' + med_info['Season'].zfill(2) +
                        'E' + med_info['Episode'].zfill(2) + ' - ' +
                        med_info['Title'] + ext)
            shutil.move(item, (os.path.join(os.path.dirname(item), new_name)))
        else:
            files_no_response.append(item)

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])

        if strtobool(med_info['Response']):
            new_name = (reg_dict['title'] + '(' + med_info['Year'] + ')' + ext)
            shutil.move(item, (os.path.join(os.path.dirname(item), new_name)))
        else:
            files_no_response.append(item)

if files_no_response:
    print('Files without a response:', files_no_response)
