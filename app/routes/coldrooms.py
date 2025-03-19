from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import ColdRoom, Location

coldrooms_bp = Blueprint("coldrooms", __name__)

@coldrooms_bp.route("/coldrooms", methods=["GET"])
#@login_required
def coldrooms():
    search_query = request.args.get("search", "").strip()  # Récupère la recherche

    if search_query:
        coldrooms = ColdRoom.select().where(ColdRoom.coldroom_name.contains(search_query))  
    else:
        coldrooms = ColdRoom.select()  # Si pas de recherche, on affiche tout

    return render_template("coldrooms.html", coldrooms=coldrooms, search_query=search_query)

@coldrooms_bp.route("/coldrooms/view/<int:id>", methods=["GET", "POST"])
def coldrooms_view(id):
    coldroom = ColdRoom.get_or_none(ColdRoom.id_coldroom == id)
    locations = Location.select().where(Location.id_coldroom == coldroom)
    if not coldroom:
        flash("Chambre froide introuvable.", "danger")
        return redirect(url_for("coldrooms.coldrooms"))

    return render_template("coldrooms_view.html", coldroom=coldroom, locations=locations)