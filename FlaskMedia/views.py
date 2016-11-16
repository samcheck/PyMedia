from flask import render_template, flash, redirect, session, url_for, request, send_from_directory
from FlaskMedia import app, db
from .models import Series, Episode, Movie

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


@app.route('/movie')
def all_Movies():
    available_movies = Movie.query.all()
    return render_template('all_Movies.html', Movies=available_movies)


@app.route('/movie/<title>(<year>)')
def Movies(title, year):
    movie = Movie.query.filter_by(title=title, year=year).first()
    if not TV:
        flash('Movie: %s (%s) not found in database.' % (title, year))
        return redirect(url_for('index'))
    return render_template('movie.html', movie=movie)


@app.route('/tv')
def TVseries():
    available_series = Series.query.all()
    return render_template('TVseries.html', title='TV shows', Series=available_series)


@app.route('/tv/<series_title>')
def TV(series_title):
    TV = Series.query.filter_by(title=series_title).first()
    if not TV:
        flash('TV series: %s not found in database.' % series_title)
        return redirect(url_for('index'))
    eps = Episode.query.filter_by(series_id=TV.id).all()
    return render_template('TVshow.html', title=series_title, episodes=eps)


@app.route('/tv/<series_title>/S<season>/E<episode>')
def EP(series_title, season, episode):
    TV = Series.query.filter_by(title=series_title).first()
    ep = Episode.query.filter_by(season=season, episode=episode, series_id=TV.id).first()
    if not ep:
        flash('Episode for: %s S%sE%s not found in database.' % (series_title, season, episode))
        return redirect(url_for('index'))
    return render_template('episode.html', episode=ep)


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server = request.environ.get('werkzeug.server.shutdown')
    if shutdown_server is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_server()
    return 'Server shutting down...'


@app.route('/uploads/<path:filename>')
def hosted(filename):
    return send_from_directory('/mnt/Programs/imgs/', filename)
