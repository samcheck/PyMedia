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
import mff

def main():
    # set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='whats_on_tv.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input directory to search.')
    parser.add_argument('-t', '--time', help='Viewing time in minutes')
    args = parser.parse_args()
    if args.input:
        in_path = args.input
    else:
        parser.print_help()
        sys.exit(1)

    # One time loop to generate a list of available media files in path
    m_list = []
    for item in videoLister.videoDir(in_path):
        #logger.info("Found: {}".format(item)) # Can write really long log files
        m_list.append(item)

    # Randomly select a video to play

    if args.time: # Find a file with a duration shorter than allotted time
        duration = 999
        while duration > int(args.time):
            choice = random.choice(m_list)
            m_list.remove(choice) # remove the choice from the list
            m_file = mff.format_info(choice) # get file details
            duration = round(float(m_file['duration']) / 60) # convert to integer minutes
            logger.info("Selected: {}".format(os.path.basename(choice)))
            logger.info("Running time: {} min".format(duration))
    else:
        choice = random.choice(m_list)

    logger.info("Playing: {}".format(os.path.basename(choice)))

    # Launch selected video with MPV in full screen
    play_command = 'mpv "{}" --really-quiet --fs &'.format(choice)
    proc = subprocess.Popen(shlex.split(play_command))
    # use proc.terminate() to kill


if __name__ == '__main__':
    main()
