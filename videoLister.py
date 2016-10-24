#!/usr/bin/python3
# videoLister.py - walk a given directory and return list of files matching
# the given extensions

import os

VIDEO_EXT = ('.webm', '.mkv', '.flv', '.avi', '.mov', '.qt', '.wmv', '.mp4',
             '.m4v', '.mpg', '.mpeg')


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
    if not(os.path.exists(path_to_videos) and os.path.isdir(path_to_videos)):
        raise Exception('Not a valid directory, please input a directory to search.')

    for root, dirs, files in os.walk(path_to_videos):
        for filename in files:
            if filename.endswith(VIDEO_EXT):
                yield os.path.join(root, filename)
