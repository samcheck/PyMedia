#!venv/bin/python3
from FlaskMedia import db
from FlaskMedia.models import Series
from FlaskMedia.models import Episode

for ep in Episode.query.all():
    db.session.delete(ep)

for series in Series.query.all():
    db.session.delete(series)

db.session.commit()
