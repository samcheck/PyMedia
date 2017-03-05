#!venv/bin/python3
# media_namer.py - Renames passed media files in a folder (and subfolders) using
#                   OMDB for movies and theTVDB for TV shows

import sys
import os
import logging
import argparse
import random

import videoLister

def main():
    # set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='whats_on_tv.log', filemode='w', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input directory to clone.')
    args = parser.parse_args()
    if args.input:
        in_path = args.input
    else:
        parser.print_help()
        sys.exit(1)

    mList = []

    for item in videoLister.videoDir(in_path):
        logger.info("Found: {}.".format(item))
        mList.append(item)

    choice = random.choice(mList)
    logger.info("Playing: {}".format(os.path.basename(choice)))

    command = 'mpv "{}" --really-quiet &'.format(choice)
    os.system(command)

if __name__ == '__main__':
    main()
