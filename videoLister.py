#!/usr/bin/python3
# videoLister.py - walk a given directory and return list of files matching
# the given extensions

import os

VIDEO_EXT = ('.webm', '.mkv', '.flv', '.avi', '.mov', '.qt', '.wmv', '.mp4',
             '.m4v', '.mpg', '.mpeg')


def videoDir(pathToVideos):
    """Searches directory and generates a list of matching filenames.

    Argument:
        pathToVideos: path to search for files matching the defined video
            extensions.

    Returns:
        videoList: a list of matching filenames, including path.

    Raises:
        Exception: Not a valid directory, please input a directory to search.
    """
    if not(os.path.exists(pathToVideos) and os.path.isdir(pathToVideos)):
        raise Exception('Not a valid directory, please input a directory to search.')

    videoList = []
    for root, dirs, files in os.walk(pathToVideos):
        for filename in files:
            if filename.endswith(VIDEO_EXT):
                videoList.append((os.path.join(root, filename)))

    return(videoList)
