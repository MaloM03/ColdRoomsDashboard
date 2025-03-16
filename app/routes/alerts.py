from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Alert

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts")
def alerts():
    # Récupération des paramètres de tri depuis l'URL (GET)
    sort_by = request.args.get("sort_by", "created_at")  # Default: date de création
    order = request.args.get("order", "desc")  # Default: décroissant

    # Vérification pour éviter les valeurs non autorisées
    valid_sort_by = ["created_at", "updated_at"]
    valid_order = ["asc", "desc"]

    if sort_by not in valid_sort_by:
        sort_by = "created_at"

    if order not in valid_order:
        order = "desc"

    # Appliquer le tri
    if order == "asc":
        alerts_list = Alert.select().order_by(getattr(Alert, sort_by).asc())
    else:
        alerts_list = Alert.select().order_by(getattr(Alert, sort_by).desc())

    return render_template("alerts.html", alerts=alerts_list, sort_by=sort_by, order=order)