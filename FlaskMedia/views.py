import datetime

from flask import render_template, flash, redirect, session, url_for, request, send_from_directory
from FlaskMedia import app, db
from .models import Series, Episode, Movie
from .forms import EditMovieForm
from sqlalchemy.sql import func

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    rand_query = Movie.query.order_by(func.random()).limit(3)
    return render_template('index.html', title='Home', carousel_items=rand_query)


@app.route('/movie')
def Movie_all():
    available_movies = Movie.query.all()
    return render_template('Movie_all.html', movies=available_movies)


@app.route('/movie/<title>(<year>)', methods=['GET', 'POST'])
def Movies(title, year):
    movie = Movie.query.filter_by(title=title, year=year).first()
    if not movie:
        flash('Movie: %s (%s) not found in database.' % (title, year), 'danger')
        return redirect(url_for('Movie_all'))

    form = EditMovieForm()
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.plot = form.plot.data
        movie.last_updated_utc = datetime.datetime.utcnow()
        db.session.add(movie)
        db.session.commit()
        flash('Changes to %s (%s) have been saved.' % (title, year), 'success')
        return redirect(url_for('Movies', title=movie.title, year=movie.year))
    else:
        form.title.data = movie.title
        form.plot.data = movie.plot
    return render_template('movie.html', form=form, movie=movie)


@app.route('/movie/<title>(<year>)/edit', methods=['GET', 'POST'])
def edit_movie(title, year):
    movie = Movie.query.filter_by(title=title, year=year).first()
    if not movie:
        flash('Movie: %s (%s) not found in database.' % (title, year), 'danger')
        return redirect(url_for('Movie_all'))

    form = EditMovieForm()
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.plot = form.plot.data
        movie.last_updated_utc = datetime.datetime.utcnow()
        db.session.add(movie)
        db.session.commit()
        flash('Changes to %s (%s) have been saved.' % (title, year), 'success')
        return redirect(url_for('Movies', title=movie.title, year=movie.year))
    else:
        form.title.data = movie.title
        form.plot.data = movie.plot
    return render_template('edit_movie.html', form=form, movie=movie)


@app.route('/movie/<title>(<year>)/delete')
def delete_movie(title, year):
    movie = Movie.query.filter_by(title=title, year=year).first()
    if not movie:
        flash('Movie: %s (%s) not found in database.' % (title, year), 'danger')
        return redirect(url_for('Movie_all'))
    db.session.delete(movie)
    db.session.commit()
    flash('Movie: %s (%s) has been deleted.' % (title, year), 'success')
    return redirect(url_for('Movie_all'))


@app.route('/tv')
def TVseries():
    available_series = Series.query.all()
    return render_template('TVseries.html', title='TV shows', Series=available_series)


@app.route('/tv/<series_title>')
def TV(series_title):
    TV = Series.query.filter_by(title=series_title).first()
    if not TV:
        flash('TV series: %s not found in database.' % series_title, 'danger')
        return redirect(url_for('index'))
    eps = Episode.query.filter_by(series_id=TV.id).all()
    return render_template('TVshow.html', title=series_title, series=TV, episodes=eps)


@app.route('/tv/<series_title>/S<season>/E<episode>')
def EP(series_title, season, episode):
    TV = Series.query.filter_by(title=series_title).first()
    ep = Episode.query.filter_by(season=season, episode=episode, series_id=TV.id).first()
    if not ep:
        flash('Episode for: %s S%sE%s not found in database.' % (series_title, season, episode), 'danger')
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
