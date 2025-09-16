from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.tarea import Tarea
from models.usuario import db
from routes.rutas_usuario import login_requerido

tarea_bp = Blueprint("tarea", __name__)

@tarea_bp.route("/")
@login_requerido
def lista_tareas():
    tareas = Tarea.query.filter_by(id_usuario=session["id_usuario"]).all()
    return render_template("lista_tareas.html", tareas=tareas)

@tarea_bp.route("/tarea/agregar", methods=["GET", "POST"])
@login_requerido
def agregar_tarea():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion, id_usuario=session["id_usuario"])
        db.session.add(nueva_tarea)
        db.session.commit()
        flash("Tarea agregada", "success")
        return redirect(url_for("tarea.lista_tareas"))
    return render_template("agregar_tarea.html")

@tarea_bp.route("/tarea/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    if tarea.id_usuario != session["id_usuario"]:
        flash("No puedes editar esta tarea", "error")
        return redirect(url_for("tarea.lista_tareas"))

    if request.method == "POST":
        tarea.titulo = request.form["titulo"]
        tarea.descripcion = request.form["descripcion"]
        tarea.estado = "estado" in request.form
        db.session.commit()
        flash("Tarea actualizada", "success")
        return redirect(url_for("tarea.lista_tareas"))

    return render_template("editar_tarea.html", tarea=tarea)

@tarea_bp.route("/tarea/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    if tarea.id_usuario != session["id_usuario"]:
        flash("No puedes eliminar esta tarea", "error")
        return redirect(url_for("tarea.lista_tareas"))
    db.session.delete(tarea)
    db.session.commit()
    flash("Tarea eliminada", "success")
    return redirect(url_for("tarea.lista_tareas"))