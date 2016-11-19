#!venv/bin/python3
import os
import sys
import logging
import datetime
from distutils.util import strtobool

from tqdm import tqdm

import videoLister
import scrapeOMDB
import regSplit

from FlaskMedia import db
from FlaskMedia.models import Movie

logger = logging.getLogger(__name__)
logging.basicConfig(filename='write_to_db_movie.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


in_path = ' '.join(sys.argv[1:])


def write_movie(title, plot, year, released, last_updated_utc, rated, runtime,
                IMDB_id, IMDB_rating, IMDB_rating_count, metascore, awards,
                language, country, poster):

    movie = Movie(title=title, plot=plot, year=year, released=released,
                  last_updated_utc=last_updated_utc, rated=rated,
                  runtime=runtime, IMDB_id=IMDB_id, IMDB_rating=IMDB_rating,
                  IMDB_rating_count=IMDB_rating_count, metascore=metascore,
                  awards=awards, language=language, country=country,
                  poster=poster)

    # attempted to use try/except to catch errors but did not work on SQL errors
    if not Movie.query.filter_by(title=title, year=year).first():
        db.session.add(movie)
        logger.info("Wrote Movie: %s" % movie)
        db.session.commit()
    else:
        logger.warning("Movie %s already in database." % movie)



for item in tqdm(videoLister.videoDir(in_path)):
    reg_dict = regSplit.Split(item)
    path = os.path.abspath(item)
    logger.info("Working on: %s" % path)

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
            logger.warning('File not found: %s' % item)

    else:
        logger.warning('File not added: %s' % item)
