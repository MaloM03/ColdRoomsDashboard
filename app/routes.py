from flask import render_template

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return "<h1>À propos de cette application</h1>"
