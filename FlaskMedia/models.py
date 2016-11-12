from FlaskMedia import db

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    plot = db.Column(db.String(2048), index=True)
    episodes = db.relationship('Episode', backref='series', lazy='dynamic')

    def __repr__(self):
        return '<Series %r>' % (self.title)


class Episode(db.Model):
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
        return '<S%sE%s - %r>' % (self.season, self.episode, self.title)
