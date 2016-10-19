# PyMedia
My attempt to build a small media database to query and display media data

TODO:
- [x] Get media to scrape: videoLister.py
- [x] Scrape media data: scrapeOMDB.py provides that functionality
- [ ] Build database: in progress, determining the best way to store the individual
 json returns that currently come from scrapeOMDB
    - Options:
      - individual jsons; unwieldy with large media db
      - csv; can store keys/values with csv.DictWriter/Reader, not ideal
      - xml; switch to getting data in xml format from scrapeOMDB, build master xml file,
      may have same issues as jsons
      - some flavor of SQL; need to set up and build a SQL db...
- [ ] Display the media information: some locally hosted front-end to display media
available in db


OVERALL:
- a lot of validation and error/exception checking
- automation options
- refactoring
