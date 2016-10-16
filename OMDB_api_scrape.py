#!/usr/bin/python3
# OMDB_api_scrape.py - parses a movie and year from the command line, grabs the
#                      xml and saves a copy for later

import pprint, requests, sys, os
import lxml.etree
from xml.dom.minidom import parseString

URL_BASE = 'http://www.omdbapi.com/?'

if len(sys.argv) > 1:
	# Get address from command line.
    mTitle = '+'.join(sys.argv[1:-1]) # need to correctly format the title str
    mYear = sys.argv[-1]
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

# make sure the xml is correctly parsed
theXML = parseString(response.text)

# Save the XML file in current directory as Movie_Title_Year.xml from sys.argv
with open((os.path.join(os.getcwd(), ('_'.join(sys.argv[1:]) + '.xml'))), 'w') as outfile:
    outfile.write(theXML.toxml())
