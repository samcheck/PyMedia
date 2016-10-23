#!/usr/bin/python3
# tv_namer.py - Renames passed media files of TV shows

import shutil
import os
import sys
import tqdm
from distutils.util import strtobool
import videoLister
import scrapeTVDB
import regSplit

in_path = ' '.join(sys.argv[1:])

media_list = videoLister.videoDir(in_path)
files_not_renamed = []
for item in tqdm.tqdm(media_list):
    reg_dict = regSplit.Split(item)
    ext = os.path.splitext(item)[1]

    if reg_dict['type'] == 'tv':
        med_info = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'])

        new_name = (reg_dict['title'] + ' S' + reg_dict['season'].zfill(2) +
                        'E' + reg_dict['episode'].zfill(2) + ' - ' +
                        med_info['data'][0]['episodeName'] + ext)
        shutil.move(item, (os.path.join(os.path.dirname(item), new_name)))

    else:
        files_not_renamed.append(item)

if files_not_renamed:
    print('Files not renamed:', files_not_renamed)
