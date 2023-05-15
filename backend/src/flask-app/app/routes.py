from app import app

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/about')
def about():
    return "This is the About page"
