from FlaskMedia import db

class TVshow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, index=True)
    episode = db.Column(db.Integer, index=True)
    series_title = db.Column(db.String(256), index=True)
    ep_title = db.Column(db.String(256), index=True)
    plot = db.Column(db.String(2048), index=True)

    def __repr__(self):
        return '<Episode %r>' % (self.ep_title)
