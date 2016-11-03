from flask import render_template
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
