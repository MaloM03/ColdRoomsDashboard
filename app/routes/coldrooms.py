from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import ColdRoom, Location, Temperature

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
    if not coldroom:
        flash("Chambre froide introuvable.", "danger")
        return redirect(url_for("coldrooms.coldrooms"))
    
    # Récupérer les locations
    locations = Location.select().where(Location.id_coldroom == coldroom)
    
    # Récupérer les températures
    temperatures = (Temperature
                    .select()
                    .where(Temperature.id_coldroom == coldroom)
                    .order_by(Temperature.temp_date.asc())
                    .limit(100))
    
    # Préparer les données pour le graphique
    temp_dates = [temp.temp_date.strftime('%Y-%m-%d %H:%M:%S') for temp in temperatures]
    temp_values = [float(temp.temperature) for temp in temperatures]
    
    return render_template("coldrooms_view.html", 
                          coldroom=coldroom, 
                          locations=locations,
                          temp_dates=temp_dates,
                          temp_values=temp_values,
                          min_limit=float(coldroom.temp_min_limit) if coldroom.temp_min_limit else None,
                          max_limit=float(coldroom.temp_max_limit) if coldroom.temp_max_limit else None)