#!venv/bin/python3
# media_namer.py - Renames passed media files in a folder (and subfolders) using
#                   OMDB for movies and theTVDB for TV shows

import sys
import os
import logging
import argparse
import random
import subprocess
import shlex

import videoLister

def main():
    # set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='whats_on_tv.log', filemode='w', level=logging.WARNING,
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

    # One time loop to generate a list of available media files in path
    mList = []
    for item in videoLister.videoDir(in_path):
        logger.info("Found: {}".format(item))
        mList.append(item)

    # Randomly select a video to play
    choice = random.choice(mList)
    logger.info("Playing: {}".format(os.path.basename(choice)))

    # Launch selected video with MPV in full screen
    command = 'mpv "{}" --really-quiet --fs &'.format(choice)
    proc = subprocess.Popen(shlex.split(command))
    # use proc.terminate() to kill


if __name__ == '__main__':
    main()
