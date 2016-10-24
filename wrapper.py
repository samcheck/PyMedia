#!/usr/bin/python3
# wrapper.py - get video path from command line inputs, combine together other
# functions to build media db, in individual csv files

import sys
import csv
import tqdm
from distutils.util import strtobool
import regSplit
import scrapeOMDB
import videoLister

in_path = ' '.join(sys.argv[1:])

files_no_response = []
for item in tqdm.tqdm(videoLister.videoDir(in_path)):
    reg_dict = regSplit.Split(item)

    if reg_dict['type'] == 'tv':
        med_info = scrapeOMDB.OMDBtv(reg_dict['title'], reg_dict['season'],
                                    reg_dict['episode'])
        if strtobool(med_info['Response']):
            out_file = (reg_dict['title'] + '_S' + med_info['Season'].zfill(2) +
                        'E' + med_info['Episode'].zfill(2) + '.csv')
        else:
            files_no_response.append(item)

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])
        if strtobool(med_info['Response']):
            out_file = (reg_dict['title'] + '_' + med_info['Year'] + '.csv')
        else:
            files_no_response.append(item)

    with open(out_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(med_info))
        writer.writeheader()
        writer.writerow(med_info)

print('Files without a response:', files_no_response)
