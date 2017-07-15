#!venv/bin/python3
# playtime.py - calculates playtime for a file or directory of media files using
#               ffprobe and custom wrapper

import logging
import argparse
import os

import mff  # this is the custom ffprobe wrapper to get duration info.
import videoLister  # video directory lister

def get_duration(media):
    logger = logging.getLogger('get_duration')
    f = mff.format_info(media)
    if f['duration']:
        return float(f['duration'])
    else:
        logger.info('No duration info for {}'.format(os.path.splitext(media)[0]))
        return 0

def human_time(seconds):
    secs = seconds % 60
    mins = (seconds % 3600) // 60
    hours = (seconds % 86400) // 3600
    days = seconds // 86400
    return{'days': days, 'hours': hours, 'minutes': mins, 'seconds': secs}

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='playtime.log',level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file or directory.')
    parser.add_argument('-t', '--time', action='store_true', help='Output human readable time')
    args = parser.parse_args()
    if args.input:
        in_path = args.input
    else:
        parser.print_help()
        sys.exit(1)

    time = 0    # seconds
    for item in videoLister.videoDir(in_path):
        t_new = get_duration(item)
        time = time + t_new

    if args.time:
        out = human_time(time)
        print('{} days, {}:{}:{}'.format(int(out['days']), int(out['hours']),
            int(out['minutes']), int(out['seconds'])))

    else:
        print(time)

if __name__ == "__main__":
    main()
