#!/usr/bin/python3
# videoLister.py - walk a given directory and return list of files matching
# the given extensions

import os
import logging

VIDEO_EXT = ('.webm', '.mkv', '.flv', '.avi', '.mov', '.qt', '.wmv', '.mp4',
             '.m4v', '.mpg', '.mpeg')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def videoDir(path_to_videos):
    """Searches directory and generates a list of matching filenames.

    Argument:
        path_to_videos: path to search for files matching the defined video
            extensions.

    Yields:
        A matching filename, including path.

    Raises:
        Exception: Not a valid directory, please input a directory to search.
    """

    if os.path.exists(path_to_videos) and os.path.isdir(path_to_videos):
        for root, dirs, files in os.walk(path_to_videos):
            for filename in files:
                if filename.endswith(VIDEO_EXT):
                    yield os.path.join(root, filename)

    elif os.path.exists(path_to_videos) and os.path.isfile(path_to_videos):
        if path_to_videos.endswith(VIDEO_EXT):
            yield path_to_videos

    elif not (os.path.exists(path_to_videos) and (os.path.isdir(path_to_videos) or os.path.isfile(path_to_videos))):
        logger.warning('%s is not a valid directory or file.' % path_to_videos)
