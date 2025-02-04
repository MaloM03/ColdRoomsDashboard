from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importation des routes
    from app.routes import init_routes
    init_routes(app)

    return app
