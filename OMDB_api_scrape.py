#!/usr/bin/python3
# OMDB_api_scrape.py - parses a movie and year from the command line, grabs the
#                      xml and saves a copy for later

import requests, sys, os
import lxml.etree

URL_BASE = 'http://www.omdbapi.com/?'

if len(sys.argv) > 1:
	# Get address from command line.
    mTitle = '+'.join(sys.argv[1:-1])
    mYear = sys.argv[-1]
    print(mTitle)
    print(mYear)
else:
    print("Usage: OMDB_api_scrape.py <Movie Title> <Year>")
    sys.exit(1)

# Craft the URL
url = URL_BASE + 't=' + mTitle + '&y=' + mYear + '&plot=full&r=xml'

# Try to get the url
try:
	response = requests.get(url)
	response.raise_for_status()
except requests.exceptions.RequestException as err:
	print(err)
	sys.exit(1)

# Save the XML file
with open((os.path.join(os.getcwd(), (mTitle + '_' + mYear + '.xml'))), 'wb') as outfile:
    outfile.write(response.text)
