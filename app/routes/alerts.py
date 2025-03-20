from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Alert

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts")
@login_required
def alerts():
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")
    state_filter = request.args.get("state_filter", "")  # Filtre d'état

    valid_sort_by = ["created_at", "updated_at"]
    valid_order = ["asc", "desc"]

    if sort_by not in valid_sort_by:
        sort_by = "created_at"

    if order not in valid_order:
        order = "desc"

    # Construire la requête avec filtrage de l'état si spécifié
    query = Alert.select()
    if state_filter in ["0", "1", "2"]:
        query = query.where(Alert.states == int(state_filter))

    query = query.order_by(getattr(Alert, sort_by).asc() if order == "asc" else getattr(Alert, sort_by).desc())

    return render_template("alerts.html", alerts=query, sort_by=sort_by, order=order, state_filter=state_filter)

@alerts_bp.route("/alerts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def alerts_edit(id):
    alert = Alert.get_or_none(Alert.id_alerts == id)
    if not alert:
        flash("Alerte introuvable.", "danger")
        return redirect(url_for("alerts.alerts"))

    if request.method == "POST":
        if "edit" in request.form:
            name = "user inconu"
            comment = request.form.get("comment", "").strip()
            state = request.form.get("state", "").strip()

            # Vérifications de validation
            if len(name) > 50:
                flash("Le nom ne peut pas dépasser 50 caractères.", "danger")
            elif len(comment) > 200:
                flash("Le commentaire ne peut pas dépasser 200 caractères.", "danger")
            elif state not in ["0", "1", "2"]:  # Validation de l'état
                flash("État invalide.", "danger")
            else:
                alert.name = name
                alert.comment = comment
                alert.states = int(state)
                alert.save()
                return redirect(url_for("alerts.alerts", id=id))

    return render_template("alerts_edit.html", alert=alert)