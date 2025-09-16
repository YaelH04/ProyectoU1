from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.usuario import db, Usuario
from functools import wraps

usuario_bp = Blueprint("usuario", __name__)

def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            flash("⚠️Debes iniciar sesión primero", "warning")
            return redirect(url_for("usuario.login"))
        return f(*args, **kwargs)
    return wrapper

# Ruta de registro de usuarios
@usuario_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        confirmar = request.form["confirmar_contraseña"]

        # Validar contraseña
        if contraseña != confirmar:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("usuario.registro"))

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, correo=correo)
        nuevo_usuario.set_contraseña(contraseña)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado con éxito", "success")
        return redirect(url_for("usuario.login"))

    return render_template("registro.html")

# Ruta de login
@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_contraseña(contraseña):
            session["id_usuario"] = usuario.id
            session["nombre_usuario"] = usuario.nombre_usuario
            flash("Bienvenido!", "success")
            return redirect(url_for("tarea.lista_tareas"))
        else:
            flash("Credenciales inválidas", "error")
    return render_template("login.html")

# Ruta de logout
@usuario_bp.route("/logout")
@login_requerido
def logout():
    session.clear()
    flash("ℹ️Sesión cerrada", "info")
    return redirect(url_for("usuario.login"))