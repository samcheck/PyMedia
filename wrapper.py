#!/usr/bin/python3
# wrapper.py - get video path from command line inputs, combine together other
# functions to build media db, in individual csv files

import sys, csv, datetime
import regSplit, scrapeOMDB, videoLister

in_path = ' '.join(sys.argv[1:])
count = 0
media_list = videoLister.videoDir(in_path)
for item in media_list:
    reg_dict = regSplit.Split(item)

    if reg_dict['type'] == 'tv':
        med_info = scrapeOMDB.OMDBtv(reg_dict['title'], reg_dict['season'], reg_dict['episode'])

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])

    count += 1
    print('%s items processed...' % str(count))
# Sort the headers into alphabetical order
    headers = sorted(med_info)
    out_file = reg_dict['title'] + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + '.csv'
    with open(out_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow(med_info)
