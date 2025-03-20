from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.database import initialize_db
from app.routes.auth import auth_bp
from app.routes.coldrooms import coldrooms_bp
from app.routes.alerts import alerts_bp
from app.routes.materials import materials_bp

from app.models import User

def create_app():
    app = Flask(__name__)

    # Charger la configuration
    app.config.from_object(Config)
    print(app.config["SECRET_KEY"])

    app.config["SECRET_KEY"] = "supersecretkey"  # Clé secrète pour les sessions

    # Initialiser la base de données
    initialize_db()

    # Initialisation de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)  # Associe login_manager avec l'app Flask
    login_manager.login_view = "auth.login"  # Redirige vers la page login en cas de non-authentification
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "danger"
    

    @login_manager.user_loader
    def load_user(user_id):
        print(f" Chargement de l'utilisateur: {user_id}")  # DEBUG

        if not user_id:  #  Évite l'erreur si user_id est None
            return None

        try:
            return User.get_or_none(User.id_users == int(user_id))
        except ValueError:
            print(" Erreur: user_id n'est pas un entier valide !")
            return None

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(coldrooms_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(materials_bp)

    return app
