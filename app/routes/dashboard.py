from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import ColdRoom

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
#@login_required
def dashboard():
    search_query = request.args.get("search", "").strip()  # Récupère la recherche

    if search_query:
        coldrooms = ColdRoom.select().where(ColdRoom.coldroom_name.contains(search_query))  
    else:
        coldrooms = ColdRoom.select()  # Si pas de recherche, on affiche tout

    return render_template("dashboard.html", coldrooms=coldrooms, search_query=search_query)