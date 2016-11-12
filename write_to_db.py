#!venv/bin/python3
import os
import sys
import logging
import datetime

from tqdm import tqdm

import videoLister
import scrapeTVDB
import regSplit

from FlaskMedia import db
from FlaskMedia.models import Series, Episode

logger = logging.getLogger(__name__)
logging.basicConfig(filename='write_to_db.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def write_ep_short(season, ep, title, plot, first_aired, last_updated_utc, TVDB_id, series_id):
    # make
    new_ep=Episode(season=season, episode=ep, title=title, plot=plot,
                   first_aired=first_aired, last_updated_utc=last_updated_utc,
                   TVDB_id=TVDB_id, series_id=series_id)
    # attempted to use try/except to catch errors but did not work on SQL errors
    if not Episode.query.filter_by(season=season, episode=episode, series_id=series_id).first():
        db.session.add(new_ep)
        logger.info("Wrote Episode: %s" % new_ep)
        db.session.commit()
    else:
        logger.warning("Episode %s already in database." % new_ep)


def write_ep_long(season, ep, title, plot, first_aired, last_updated_utc,
                  TVDB_id, IMDB_id, abs_num, TVDB_rating, TVDB_rating_count,
                  TVDB_last_update, series_id):
    # make
    new_ep=Episode(season=season, episode=ep, title=title, plot=plot,
                   first_aired=first_aired, last_updated_utc=last_updated_utc,
                   TVDB_id=TVDB_id,IMDB_id=IMDB_id, abs_num=abs_num,
                   TVDB_rating=TVDB_rating, TVDB_rating_count=TVDB_rating_count,
                   TVDB_last_update=TVDB_last_update, series_id=series_id)
    # attempted to use try/except to catch errors but did not work on SQL errors
    if not Episode.query.filter_by(season=season, episode=episode, series_id=series_id).first():
        db.session.add(new_ep)
        logger.info("Wrote Episode: %s" % new_ep)
        db.session.commit()
    else:
        logger.warning("Episode %s already in database." % new_ep)


def write_series(title):
    new_series=Series(title=title)
    # attempted to use try/except to catch errors but did not work on SQL errors
    if not Series.query.filter_by(title=series_title).first():
        db.session.add(new_series)
        logger.info("Wrote Series: %s" % series_title)
        db.session.commit()
    else:
        logger.warning("Series %s already in database." % new_series)


in_path = ' '.join(sys.argv[1:])

JWT = scrapeTVDB.auth()
for item in tqdm(videoLister.videoDir(in_path)):
    reg_dict = regSplit.Split(item)
    path = os.path.abspath(item)
    logger.info("Working on: %s" % path)

    if reg_dict['type'] == 'tv':
        ep_search = scrapeTVDB.theTVDB(reg_dict['title'], reg_dict['season'],
                                reg_dict['episode'], JWT)


        med_info = scrapeTVDB.episode_id(ep_search['data'][0]['id'], JWT)
        series_title = reg_dict['title']
        # get data using tvdb scraper
        season = med_info['data']['airedSeason']
        episode = med_info['data']['airedEpisodeNumber']
        title = med_info['data']['episodeName']
        plot = med_info['data']['overview']
        first_aired = datetime.datetime.strptime(med_info['data']['firstAired'],'%Y-%m-%d')
        last_updated_utc = datetime.datetime.utcnow()
        TVDB_id = med_info['data']['id']
        IMDB_id = med_info['data']['imdbId']
        abs_num = med_info['data']['absoluteNumber']
        TVDB_rating = med_info['data']['siteRating']
        TVDB_rating_count = med_info['data']['siteRatingCount']
        TVDB_last_update = datetime.datetime.fromtimestamp(med_info['data']['lastUpdated'])

        # search for series title in db
        series = Series.query.filter_by(title=series_title).first()
        if series: # make sure we get a match
            write_ep_long(season, episode, title, plot, first_aired,
                          last_updated_utc, TVDB_id, IMDB_id, abs_num,
                          TVDB_rating, TVDB_rating_count, TVDB_last_update,
                          series.id)
        else:
            write_series(series_title)
            series = Series.query.filter_by(title=series_title).first()
            write_ep_long(season, episode, title, plot, first_aired,
                          last_updated_utc, TVDB_id, IMDB_id, abs_num,
                          TVDB_rating, TVDB_rating_count, TVDB_last_update,
                          series.id)
    else:
        logger.warning('File not added: ', item)
