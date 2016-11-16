from FlaskMedia import db

class Series(db.Model):
    """DB structure for TV Series."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    plot = db.Column(db.String(2048), index=True)
    episodes = db.relationship('Episode', backref='series', lazy='dynamic')

    def __repr__(self):
        return '<Series %r>' % (self.title)


class Episode(db.Model):
    """DB structure for TV Episodes."""
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, index=True)
    episode = db.Column(db.Integer, index=True)
    title = db.Column(db.String(255), index=True)
    plot = db.Column(db.String(2047), index=True)
    first_aired = db.Column(db.DateTime)
    last_updated_utc = db.Column(db.DateTime)
    TVDB_id = db.Column(db.Integer, index=True)
    IMDB_id = db.Column(db.String(15), index=True)
    abs_num = db.Column(db.Integer, index=True)
    TVDB_rating = db.Column(db.Float, index=True)
    TVDB_rating_count = db.Column(db.Integer, index=True)
    TVDB_last_update = db.Column(db.DateTime)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    __table_args__ = (db.UniqueConstraint('season', 'episode', 'series_id', name='_episode_uc'),)

    def __repr__(self):
        return '<S%sE%s - %s>' % (self.season, self.episode, self.title)


class Movie(db.Model):
    """DB structure for Movies."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    plot = db.Column(db.String(2047), index=True)
    year = db.Column(db.Integer, index=True)
    released = db.Column(db.DateTime)
    last_updated_utc = db.Column(db.DateTime)
    rated = db.Column(db.String(15), index=True)
    runtime = db.Column(db.String(15), index=True)
    IMDB_id = db.Column(db.String(15), index=True)
    IMDB_rating = db.Column(db.Float, index=True)
    IMDB_rating_count = db.Column(db.Integer, index=True)
    metascore = db.Column(db.Integer, index=True)
    awards = db.Column(db.String(255), index=True)
    language = db.Column(db.String(15), index=True)
    country = db.Column(db.String(31), index=True)
    poster = db.Column(db.String(255), index=True)

    def __repr__(self):
        return '<%s (%d)>' % (self.title, self.year)
