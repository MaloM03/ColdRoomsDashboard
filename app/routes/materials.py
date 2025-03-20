from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Material

materials_bp = Blueprint("materials", __name__)

@materials_bp.route("/materials", methods=["GET"])
@login_required
def materials():
    search_query = request.args.get("search", "").strip()  # Récupère la recherche

    if search_query:
        materials = Material.select().where(
        (Material.name.contains(search_query)) | (Material.reference.contains(search_query))
    )
    else:
        materials = Material.select()   # Si pas de recherche, on affiche tout
    return render_template("materials.html", materials=materials)



@materials_bp.route("/material/create", methods=["GET", "POST"])
@login_required
def materials_create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reference = request.form.get("reference", "").strip()

        # Vérification de la longueur du nom
        if len(name) > 25:
            flash("Le nom ne peut pas dépasser 25 caractères.", "danger")
        
        elif len(reference) > 25:
            flash("La référence ne peut pas dépasser 25 caractères.", "danger")

        # Vérification de l'unicité de la référence
        elif Material.get_or_none(Material.reference == reference):
            flash("Cette référence existe déjà. Veuillez en choisir une autre.", "danger")

        # Si tout est bon, on crée le matériau
        else:
            Material.create(name=name, reference=reference)
            return redirect(url_for("materials.materials"))

    return render_template("materials_create.html")

@materials_bp.route("/materials/edit/<int:id>", methods=["GET", "POST"])
@login_required
def materials_edit(id):
    material = Material.get_or_none(Material.id_materials == id)
    if not material:
        flash("Matériau introuvable.", "danger")
        return redirect(url_for("materials.materials"))

    if request.method == "POST":
        if "edit" in request.form: 
            name = request.form.get("name", "").strip()
            reference = request.form.get("reference", "").strip()

            # Vérifie si la référence existe déjà (hors celle en cours d'édition)
            existing_material = Material.get_or_none((Material.reference == reference) & (Material.id_materials != id))
            if existing_material:
                flash("Cette référence existe déjà !", "danger")
            elif len(name) > 25:
                flash("Le nom ne peut pas dépasser 25 caractères.", "danger")
            elif len(reference) > 25:
                flash("La référence ne peut pas dépasser 25 caractères.", "danger")
            else:
                material.name = name
                material.reference = reference
                material.save()
                return redirect(url_for("materials.materials", id=id))

        if "delete" in request.form:
            material.delete_instance()
            return redirect(url_for("materials.materials"))

    return render_template("materials_edit.html", material=material)