from flask import render_template

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/alerts')
    def alerts():
        return render_template('alerts.html')