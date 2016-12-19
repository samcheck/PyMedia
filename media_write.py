#!venv/bin/python3
import logging

from FlaskMedia import db
from FlaskMedia.models import Movie, Series, Episode

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
    if not Episode.query.filter_by(season=season, episode=ep, series_id=series_id).first():
        db.session.add(new_ep)
        logger.info("Wrote Episode: %s" % new_ep)
        db.session.commit()
    else:
        logger.warning("Episode %s already in database." % new_ep)


def write_series(title, plot, rated, IMDB_id, TVDB_rating, TVDB_rating_count,
                 TVDB_last_update, first_aired, last_updated_utc, poster,
                 network):

    new_series=Series(title=title, plot=plot, rated=rated, IMDB_id=IMDB_id,
                      TVDB_rating=TVDB_rating, TVDB_rating_count=TVDB_rating_count,
                      TVDB_last_update=TVDB_last_update, first_aired=first_aired,
                      last_updated_utc=last_updated_utc, poster=poster, network=network)
    # attempted to use try/except to catch errors but did not work on SQL errors
    if not Series.query.filter_by(title=title).first():
        db.session.add(new_series)
        logger.info("Wrote Series: %s" % title)
        db.session.commit()
    else:
        logger.warning("Series %s already in database." % new_series)
