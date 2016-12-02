
import json
import subprocess
import sys, os
import shlex
from pprint import pprint

in_path = ' '.join(sys.argv[1:])


def ffprobe_json(media_file):
    ffcom = 'ffprobe -v quiet -print_format json -show_format -show_streams'
    ff = (ffcom + " '" + media_file + "'")
    process = subprocess.Popen(shlex.split(ff), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    rc = process.poll()
    j_out = json.loads(str(stdout,'utf-8'))
    return j_out, rc

def main():
    jffop, rc = ffprobe_json(in_path)

    pprint(jffop['format']) # gen info
    for stream in range(len(jffop['streams'])):
        if jffop['streams'][stream]['codec_type'] == 'video':
            pprint(jffop['streams'][stream]['codec_name']) # video codec name
            pprint(jffop['streams'][stream]['coded_width']) # video width
        if jffop['streams'][stream]['codec_type'] == 'audio':
            pprint(jffop['streams'][stream]['codec_name']) # audio codec name

if __name__ == "__main__":
    main()
