#!/usr/bin/python3

import sys, csv, datetime

in_path = ' '.join(sys.argv[1:])

with open((in_path), 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
