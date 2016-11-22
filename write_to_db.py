#!venv/bin/python3
import os
import sys
import logging
import datetime
from distutils.util import strtobool

from tqdm import tqdm

import videoLister
import scrapeTVDB
import scrapeOMDB
import regSplit
from media_write import write_ep_long, write_series, write_movie

from FlaskMedia import db
from FlaskMedia.models import Series

logger = logging.getLogger(__name__)
logging.basicConfig(filename='write_to_db.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
            series_search = scrapeTVDB.series_search(series_title, JWT)
            series_info = scrapeTVDB.series_id(series_search['data'][0]['id'], JWT)

            series_title = series_info['data']['seriesName']
            series_plot = series_info['data']['overview']
            series_rated = series_info['data']['rating']
            series_IMDB_id = series_info['data']['imdbId']
            series_TVDB_rating = series_info['data']['siteRating']
            series_TVDB_rating_count = series_info['data']['siteRatingCount']
            series_TVDB_last_update = datetime.datetime.fromtimestamp(series_info['data']['lastUpdated'])
            series_first_aired = datetime.datetime.strptime(series_info['data']['firstAired'],'%Y-%m-%d')
            series_last_updated_utc = datetime.datetime.utcnow()
            series_poster = ('http://thetvdb.com/banners/' + series_info['data']['banner'])
            series_network = series_info['data']['network']

            write_series(series_title, series_plot, series_rated,
                         series_IMDB_id, series_TVDB_rating,
                         series_TVDB_rating_count, series_TVDB_last_update,
                         series_first_aired, series_last_updated_utc,
                         series_poster, series_network)

            series = Series.query.filter_by(title=series_title).first()
            write_ep_long(season, episode, title, plot, first_aired,
                          last_updated_utc, TVDB_id, IMDB_id, abs_num,
                          TVDB_rating, TVDB_rating_count, TVDB_last_update,
                          series.id)

    if reg_dict['type'] == 'movie':
        med_info = scrapeOMDB.OMDBmovie(reg_dict['title'], reg_dict['year'])
        if strtobool(med_info['Response']):
            # get data using OMDB scraper
            title = med_info['Title']
            plot = med_info['Plot']
            year = int(med_info['Year'])
            released = datetime.datetime.strptime(med_info['Released'],'%d %b %Y')
            last_updated_utc = datetime.datetime.utcnow()
            rated = med_info['Rated']
            runtime = med_info['Runtime']
            IMDB_id = med_info['imdbID']
            if med_info['imdbRating'].isdigit():
                IMDB_rating = med_info['imdbRating'] # need to check if N/A before convert to float
            else:
                IMDB_rating = 0
            if med_info['imdbRating'].isdigit():
                IMDB_rating_count = med_info['imdbVotes'] #need to parse string remove , before convert to int
            else:
                IMDB_rating_count = 0
            if med_info['Metascore'].isdigit():
                metascore = med_info['Metascore'] # need to check if N/A before convert to int
            else:
                metascore = 0
            awards = med_info['Awards']
            language = med_info['Language']
            country = med_info['Country']
            poster = med_info['Poster']

            write_movie(title, plot, year, released, last_updated_utc, rated,
                runtime, IMDB_id, IMDB_rating, IMDB_rating_count, metascore,
                awards, language, country, poster)

    else:
        logger.warning('File not added: %s' % item)
