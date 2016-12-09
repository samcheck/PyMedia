
import json
import subprocess
import sys, os
import shlex


def ffprobe_json(media_file):
    ffcom = 'ffprobe -v quiet -print_format json -show_format -show_streams'
    ff = (ffcom + " '" + media_file + "'")
    process = subprocess.Popen(shlex.split(ff), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    rc = process.poll()
    j_out = json.loads(str(stdout,'utf-8'))
    return j_out, rc


def ff_conv_container(media_file):
    new_name = os.path.splitext(media_file)[0]
    #-movflags +faststart (to play partial files where end is not finished)
    j, rc = ffprobe_json(media_file)
    for stream in range(len(j['streams'])):
        if j['streams'][stream]['codec_type'] == 'video':
            v_codec = j['streams'][stream]['codec_name'] # video codec name
        if j['streams'][stream]['codec_type'] == 'audio':
            a_codec = j['streams'][stream]['codec_name'] # audio codec name
            
    if v_codec == 'h264' and (a_codec == 'aac' or 'mp3'):
        codecs = '-vcodec copy -acodec copy'
    else:
        codecs = '-c:v libx264 -c:a aac'
    ff = ('ffmpeg -i "{}" {} "{}".mp4').format(media_file, codecs, new_name)
    process = subprocess.Popen(shlex.split(ff), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    rc = process.poll()
    return rc

def video_info(media_file):
    j, rc = ffprobe_json(media_file)
    for stream in range(len(j['streams'])):
        if j['streams'][stream]['codec_type'] == 'video':
            v_codec = j['streams'][stream]['codec_name'] # video codec name
            v_width = j['streams'][stream]['coded_width'] # video width
            v_height = j['streams'][stream]['coded_height'] # video height
    return{'v_codec': v_codec, 'v_width': v_width, 'v_height': v_height}


def audio_info(media_file):
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
    j, rc = ffprobe_json(media_file)
    f_name = j['format']['filename'] # full path with filename
    f_format = j['format']['format_name'] # format/contatiner
    f_duration = j['format']['duration'] # duration (in sec)
    f_size = j['format']['size'] # size info (in bytes)
    f_bitrate = j['format']['bit_rate'] # bit rate info (seems inaccurate)
    return{'name': f_name, 'format': f_format, 'duration': f_duration, 'size': f_size, 'bitrate': f_bitrate}

def main():
    media_file = ' '.join(sys.argv[1:])
    if os.path.isfile(media_file):
        v = video_info(media_file)
        a = audio_info(media_file)
        f = format_info(media_file)
        for k, s in v.items():
            print(k,s)
        for k, s in a.items():
            print(k,s)
        for k, s in f.items():
            print(k,s)

    #    ff_conv_container(media_file)

    else:
        return None


if __name__ == "__main__":
    main()
