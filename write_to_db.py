#!venv/bin/python3
import os
import sys
import logging

import videoLister
import scrapeTVDB
import regSplit

from FlaskMedia import db
from FlaskMedia.models import Series, Episode

logger = logging.getLogger(__name__)
logging.basicConfig(filename='write_to_db.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def write_ep(season, ep, title, plot, series_id):
    # make
    new_ep=Episode(season=season, episode=ep, title=title, plot=plot, series_id=series_id)
    try:
        db.session.add(new_ep)
        db.session.commit()
        logger.info("Wrote Episode: S%sE%s - %s" % (season, episode, title))
    except Exception as e:
        raise("Error adding episode to database:", e)

def write_series(title):
    new_series=Series(title=title)
    try:
        db.session.add(new_series)
        db.session.commit()
        logger.info("Wrote Series: %s" % series_title)
    except Exception as e:
        raise("Error adding season to database:", e)



in_path = ' '.join(sys.argv[1:])

files_not_added = []
for item in videoLister.videoDir(in_path):
    reg_dict = regSplit.Split(item)
    path = os.path.abspath(item)
    logger.info("Working on: %s" % path)

    if reg_dict['type'] == 'tv':
        med_info = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                reg_dict['episode'])
        series_title = reg_dict['title']
        # get data using tvdb scraper
        season = med_info['data'][0]['airedSeason']
        episode = med_info['data'][0]['airedEpisodeNumber']
        title = med_info['data'][0]['episodeName']
        plot = med_info['data'][0]['overview']

        # unused data fields from theTVDB
        # 'absoluteNumber': (int)
        # 'airedSeasonID': (int) internal TVDB reference to season
        # 'firstAired': 'YYYY-MM-DD'
        # 'id': (int) internal TVDB reference
        # 'dvdSeason': 1,
        # 'dvdEpisodeNumber': 1,

        # search for series title in db
        series = Series.query.filter_by(title=series_title).first()
        if series: # make sure we get a match
            write_ep(season, episode, title, plot, series.id)
        else:
            write_series(series_title)
            series = Series.query.filter_by(title=series_title).first()
            write_ep(season, episode, title, plot, series.id)

    else:
        files_not_added.append(item)

if files_not_added:
    logger.info('Files not added:', files_not_added)
