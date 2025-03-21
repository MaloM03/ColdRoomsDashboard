from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_login import login_user, login_required, logout_user
from app.models import User
from flask_login import current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"input username: {username}")
        print(f"input password: {password}")
        user = User.get_or_none(User.username == username)
        #user.set_password(password) # DEBUG CREER MDP ICI
        print(user)
        user.check_password(password)
        if user and user.check_password(password):
            login_user(user, remember=True)
            print("Après login_user: ", current_user.is_authenticated) # DEBUG
            print("Utilisateur ID: ", current_user.id_users)
            return redirect(url_for("coldrooms.coldrooms"))
        else:
            flash("Identifiants incorrects", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "success")
    
    # Crée une réponse avec des headers empêchant le cache
    response = make_response(redirect(url_for("auth.login")))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

