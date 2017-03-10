#!venv/bin/python3
# whats_on_tv.py - randomly selects media files to play from input directory

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
    parser.add_argument('input', help='Input directory to search.')
    # Set up range of choices starting at 15 min in 15 min increments up to 300 min
    parser.add_argument('-t', '--time', help='Viewing time in minutes', type=int, choices=range(15,301)[::15], default=300)
    parser.add_argument('-n', '--num', help='Number of videos to queue', type=int, default=1)
    args = parser.parse_args()
    if args.input:
        in_path = args.input
    else:
        parser.print_help()
        sys.exit(1)

    # One time loop to generate a list of available media files in path
    m_list = []
    for item in videoLister.videoDir(in_path):
        logger.debug("Found: {}".format(item)) # Can write really long log files
        m_list.append(item)

    # Randomly select a video to play
    random.seed()
    p_list = []
    for x in range(args.num):
        duration = 999 # Fix this, its hacky to get the loop to run...
        while duration > args.time: # Find a file with a duration shorter than allotted time
            choice = random.choice(m_list)
            m_list.remove(choice) # remove the choice from the list
            m_file = mff.format_info(choice) # get file details
            duration = round(float(m_file['duration']) / 60) # convert to integer minutes
            logger.info("Selected: {}".format(os.path.basename(choice)))
            logger.info("Running time: {} min".format(duration))

        logger.info("Added to playlist: {}".format(os.path.basename(choice)))
        p_list.append(choice)

    logger.info("Playlist: {}".format(p_list))

    # Launch selected video with MPV in full screen
    play_command = 'mpv {} --really-quiet --fs &'.format(' '.join('"{}"'.format(p) for p in p_list))
    proc = subprocess.Popen(shlex.split(play_command))
    # use proc.terminate() to kill


if __name__ == '__main__':
    main()
