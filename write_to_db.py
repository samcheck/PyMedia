#!venv/bin/python3
import os
import sys
import logging
import datetime

import videoLister
import scrapeTVDB
import regSplit

from FlaskMedia import db
from FlaskMedia.models import Series, Episode

logger = logging.getLogger(__name__)
logging.basicConfig(filename='write_to_db.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def write_ep(season, ep, title, plot, first_aired, last_updated_utc, TVDB_id, series_id):
    # make
    new_ep=Episode(season=season, episode=ep, title=title, plot=plot,
                   first_aired=first_aired, last_updated_utc=last_updated_utc,
                   TVDB_id=TVDB_id, series_id=series_id)
    try:
        db.session.add(new_ep)
        db.session.commit()
        logger.info("Wrote Episode: S%sE%s - %s" % (season, episode, title))
    except Exception as e:
        db.session.rollback()
        raise("Error adding episode to database:", e)

def write_series(title):
    new_series=Series(title=title)
    try:
        db.session.add(new_series)
        db.session.commit()
        logger.info("Wrote Series: %s" % series_title)
    except Exception as e:
        db.session.rollback()
        raise("Error adding season to database:", e)



in_path = ' '.join(sys.argv[1:])

JWT = scrapeTVDB.auth()
for item in videoLister.videoDir(in_path):
    reg_dict = regSplit.Split(item)
    path = os.path.abspath(item)
    logger.info("Working on: %s" % path)


    if reg_dict['type'] == 'tv':
        med_info = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                reg_dict['episode'], JWT)
        series_title = reg_dict['title']
        # get data using tvdb scraper
        season = med_info['data'][0]['airedSeason']
        episode = med_info['data'][0]['airedEpisodeNumber']
        title = med_info['data'][0]['episodeName']
        plot = med_info['data'][0]['overview']
        first_aired = datetime.datetime.strptime(med_info['data'][0]['firstAired'],'%Y-%m-%d')
        last_updated_utc = datetime.datetime.utcnow()
        TVDB_id = med_info['data'][0]['id']
        # unused data fields from theTVDB
        # 'absoluteNumber': (int)
        # 'airedSeasonID': (int) internal TVDB reference to season
        # 'dvdSeason': 1,
        # 'dvdEpisodeNumber': 1,

        # search for series title in db
        series = Series.query.filter_by(title=series_title).first()
        if series: # make sure we get a match
            write_ep(season, episode, title, plot, first_aired, last_updated_utc, TVDB_id, series.id)
        else:
            write_series(series_title)
            series = Series.query.filter_by(title=series_title).first()
            write_ep(season, episode, title, plot, first_aired, last_updated_utc, TVDB_id, series.id)

    else:
        logger.warning('File not added: ', item)
