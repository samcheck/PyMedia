from flask import render_template, flash, redirect
from FlaskMedia import app

@app.route('/')
@app.route('/index')
def index():
	medialist = [
	{
		'title': 'The day the earth stood still',
		'plot': 'centripedial motion stops'
	},
	{
		'title': 'The Office (US)',
		'plot': 'Michael Scott messes things up'
	}
	]
	return render_template('index.html',
							title='Home',
							medialist=medialist)

@app.route('/TV/<series_title>')
def TV(series_title):
    TV = TVshow.query.filter_by(series_title=series_title).first()
    if not TV:
        flash('TV series: %s not found in database.' % series_title)
        return redirect(url_for('index'))
    return render_template('TVshow.html', series_title=series_title)
