#!venv/bin/python3
# whats_on_tv.py - randomly selects media files to play from input directory

import sys
import os
import logging
import argparse
import random
import subprocess
import shlex
import re

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

    # Set up custom parser for viewing time range.
    def parseNumList(string):
        """
        https://stackoverflow.com/questions/6512280/accept-a-range-of-numbers-in-the-form-of-0-5-using-pythons-argparse
        """
        m = re.match(r'(\d+)(?:-(\d+))?$', string)
        start = m.group(1)
        end = m.group(2) or start
        logger.debug("List of values: {}".format([int(start), int(end)]))
        if start == end:
            return [int(start)]
        else:
            return [int(start), int(end)]

    parser.add_argument('-t', '--time', help='Viewing time in minutes', type=parseNumList, default=[300])
    parser.add_argument('-n', '--num', help='Number of videos to queue', type=int, default=1)
    parser.add_argument('-s', '--search', help='String to search for', type=str, default="")
    args = parser.parse_args()
    if args.input:
        in_path = args.input
    else:
        parser.print_help()
        sys.exit(1)

    # One time loop to generate a list of available media files in path
    m_list = []
    for item in videoLister.videoDir(in_path, args.search):
        logger.debug("Found: {}".format(item)) # Can write really long log files
        m_list.append(item)

    # Check that we matched at least args.num
    if len(m_list) == 0:
        print("Search term not found, exiting...")
        raise SystemExit
    elif len(m_list) < args.num:
        print("Number of matches found: {}, fewer than number to queue, exiting...".format(len(m_list)))
        raise SystemExit

    # set min/max durations
    if len(args.time) >= 2:
        duration_max = args.time[-1]
        duration_min = args.time[0]
    else:
        duration_max = args.time[0]
        duration_min = 0

    # Randomly select a video to play
    random.seed()
    p_list = []
    for x in range(args.num):
        duration = duration_max + 1 # Fix this, its hacky to get the loop to run...
        while duration not in range(duration_min, duration_max): # Find a file with a duration in the allotted range.
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
