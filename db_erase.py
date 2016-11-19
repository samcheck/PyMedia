#!venv/bin/python3
from FlaskMedia import db
from FlaskMedia.models import Series, Episode, Movie

for ep in Episode.query.all():
    db.session.delete(ep)

for series in Series.query.all():
    db.session.delete(series)

for mov in Movie.query.all():
    db.session.delete(mov)

db.session.commit()
