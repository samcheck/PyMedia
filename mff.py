#!venv/bin/python3
# mff.py - Wrapper for ffprobe and ffmpeg commands

import json
import subprocess
import sys
import os
import shlex
import logging
import argparse


def ffprobe_json(media_file):
    """Uses ffprobe to extract media information returning json format.

    Arguments:
        media_file: media file to be probed.

    Returns:
        json output of media information.
        return code indicating process result.

    """
    ff = 'ffprobe -v quiet -print_format json -show_format -show_streams "{}"'.format(media_file)
    process = subprocess.Popen(shlex.split(ff), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    rc = process.poll()
    j_out = json.loads(str(stdout,'utf-8'))
    return j_out, rc


def ff_to_mp4(media_file):
    """Converts a media file to h264/aac in an mp4 container.

    Arguments:
        media_file: media file to be converted.

    Returns:
        return code indicating process result.
        writes out a new media file in same directory with .mp4 extension.

    """

    logger = logging.getLogger('ff_to_mp4')
    logger.info('Converting {}'.format(os.path.splitext(media_file)[0]))

    new_name = (os.path.splitext(media_file)[0] + '_converted')
    #-movflags +faststart (to play partial files where end is not finished)
    j, rc = ffprobe_json(media_file)
    for stream in range(len(j['streams'])):
        if j['streams'][stream]['codec_type'] == 'video':
            v_codec = j['streams'][stream]['codec_name'] # video codec name
        if j['streams'][stream]['codec_type'] == 'audio':
            a_codec = j['streams'][stream]['codec_name'] # audio codec name

    if v_codec == 'h264' and a_codec == 'aac':
        logger.info('Copying media streams directly.')
        v_codec = 'copy'
        a_codec = 'copy'
    elif a_codec == 'aac':
        logger.info('Converting video stream.')
        v_codec = 'libx264'
        a_codec = 'copy'
    elif v_codec == 'h264':
        logger.info('Converting audio stream.')
        v_codec = 'copy'
        a_codec = 'aac' # could use non-free (-c:a libfdk_aac)
    else:
        logger.info('Converting both audio and video streams.')
        v_codec = 'libx264'
        a_codec = 'aac' # could use non-free (-c:a libfdk_aac)
    ff = ('ffmpeg -i "{}" -c:v {} -c:a {} "{}".mp4').format(media_file, v_codec, a_codec, new_name)
    process = subprocess.Popen(shlex.split(ff), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    rc = process.poll()
    return rc


def video_info(media_file):
    """Uses ffprobe to extract video stream information.

    Arguments:
        media_file: media file to be probed.

    Returns:
        dictionary of strings containing:
            v_codec = video codec used (h264, x265, etc.)
            v_width = video width in pixels
            v_height = video height in pixels

    """
    j, rc = ffprobe_json(media_file)
    for stream in range(len(j['streams'])):
        if j['streams'][stream]['codec_type'] == 'video':
            v_codec = j['streams'][stream]['codec_name'] # video codec name
            v_width = j['streams'][stream]['coded_width'] # video width
            v_height = j['streams'][stream]['coded_height'] # video height
    return{'v_codec': v_codec, 'v_width': v_width, 'v_height': v_height}


def audio_info(media_file):
    """Uses ffprobe to extract audio stream information.

    Arguments:
        media_file: media file to be probed.

    Returns:
        dictionary of strings containing:
            a_codec = audio codec used (aac, ac3, etc.)
            a_sample_rate = sample rate in Hertz
            a_channels = number of audio channels

    """
    j, rc = ffprobe_json(media_file)
    for stream in range(len(j['streams'])):
        if j['streams'][stream]['codec_type'] == 'audio':
            a_codec = j['streams'][stream]['codec_name'] # audio codec name
            if j['streams'][stream]['sample_rate']: #aac
                a_sample_rate = j['streams'][stream]['sample_rate'] # sample rate Hz
            elif j['streams'][stream]['bit_rate']: #ac3
                a_sample_rate = j['streams'][stream]['bit_rate'] # sample rate Hz
            a_channels = j['streams'][stream]['channels'] # number of channels
    return{'a_codec': a_codec, 'a_sample_rate': a_sample_rate, 'a_channels': a_channels}


def format_info(media_file):
    """Uses ffprobe to extract file information.

    Arguments:
        media_file: media file to be probed.

    Returns:
        dictionary of strings containing:
            name = full path with filename
            format = container type
            duration = duration in seconds
            size = file size in bytes
            bitrate = overall bitrate in bits per second

    """
    j, rc = ffprobe_json(media_file)
    
    try:
        f_name = j['format']['filename'] # full path with filename
    except KeyError:
        f_name = None

    try:
        f_format = j['format']['format_name'] # format/container
    except KeyError:
        f_format = None

    try:
        f_duration = j['format']['duration'] # duration (in sec)
    except KeyError:
        f_duration = 0

    try:
        f_size = j['format']['size'] # size info (in bytes)
    except KeyError:
        f_size = 0

    try:
        f_bitrate = j['format']['bit_rate'] # bit rate info (seems inaccurate)
    except KeyError:
        f_bitrate = 0

    return{'name': f_name, 'format': f_format, 'duration': f_duration, 'size': f_size, 'bitrate': f_bitrate}


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='mff.log',level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file.')
    parser.add_argument('-c', '--convert', action='store_true', help='Convert the file to h264/aac in mp4 container.')
    args = parser.parse_args()
    if args.input:
        media_file = args.input
    else:
        parser.print_help()
        sys.exit(1)

    # Check if input is a file and if the convert flag is passed
    if os.path.isfile(media_file):
        v = video_info(media_file)
        a = audio_info(media_file)
        f = format_info(media_file)
        for d in [v, a, f]:
            for k, s in d.items():
                print(k,s)

        if args.convert:
            ff_to_mp4(media_file)

    else:
        return None


if __name__ == "__main__":
    main()
