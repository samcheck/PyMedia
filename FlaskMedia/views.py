from flask import render_template, flash, redirect, session, url_for, request
from FlaskMedia import app, db
from .models import Series, Episode

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    available_series = Series.query.all()
    return render_template('index.html', title='Home', Series=available_series)


@app.route('/TV/<series_title>')
@app.route('/tv/<series_title>')
def TV(series_title):
    TV = Series.query.filter_by(title=series_title).first()
    if not TV:
        flash('TV series: %s not found in database.' % series_title)
        return redirect(url_for('index'))
    eps = Episode.query.filter_by(series_id=TV.id).all()
    return render_template('TVshow.html', title=series_title, episodes=eps)


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server = request.environ.get('werkzeug.server.shutdown')
    if shutdown_server is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_server()
    return 'Server shutting down...'
