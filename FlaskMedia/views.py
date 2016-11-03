from FlaskMedia import app

@app.route('/')
@app.route('/index')
def index():
	return "Flask media lives"
