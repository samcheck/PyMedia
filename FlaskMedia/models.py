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
    title = db.Column(db.String(256), index=True)
    plot = db.Column(db.String(2048), index=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))

    def __repr__(self):
        return '<Episode %r>' % (self.title)
