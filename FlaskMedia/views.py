from flask import render_template, flash, redirect, session, url_for, request
from FlaskMedia import app, db
from .models import Series, Episode

@app.route('/')
@app.route('/index')
def index():
	medialist = [
	{
		'series': {'title': 'The day the earth stood still'},
		'episode': 'centripedial motion stops'
	},
	{
		'series': {'title': 'The Office (US)'},
		'episode': 'Michael Scott messes things up'
	}
	]
	return render_template('index.html',
							title='Home',
                            episodes=medialist)


@app.route('/TV/<series_title>')
def TV(series_title):
    TV = Series.query.filter_by(title=series_title).first()
    if not TV:
        flash('TV series: %s not found in database.' % series_title)
        return redirect(url_for('index'))
    eps = [
        {'series': TV, 'title': 'Episode one a new hope'},
        {'series': TV, 'title': 'Episode two the empire strikes back'}
        ]
    return render_template('TVshow.html', Series=TV, episodes=eps)
