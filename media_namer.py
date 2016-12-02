#!/usr/bin/python3
# media_namer.py - Renames passed media files in a folder (and subfolders) using
#                   OMDB for movies and theTVDB for TV shows

import sys
import logging

import tqdm

import videoLister
import scrapeTVDB
import media_rename

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='media_namer.log',level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    in_path = ' '.join(sys.argv[1:])
    JWT = scrapeTVDB.auth()

    for item in tqdm.tqdm(videoLister.videoDir(in_path)):
        media_rename.rename(item, JWT)


if __name__ == '__main__':
    main()
