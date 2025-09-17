from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.usuario import db, Usuario
from functools import wraps
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

usuario_bp = Blueprint("usuario", __name__)

class EditProfileForm(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Actualizar Perfil')

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

        flash("ℹ️Usuario registrado con éxito", "success")
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
            flash("⚠️Credenciales inválidas", "error")
    return render_template("login.html")

# Ruta para el perfil del usuario
@usuario_bp.route("/perfil/<int:id>", methods=["GET", "POST"])
@login_requerido
def perfil(id):
    if id != session.get('id_usuario'):
        flash("No tienes permiso para editar este perfil.", "danger")
        return redirect(url_for('usuario.perfil', id=session.get('id_usuario')))

    usuario = Usuario.query.get_or_404(id)
    form = EditProfileForm()

    if form.validate_on_submit():
        usuario.nombre_usuario = form.nombre_usuario.data
        usuario.correo = form.correo.data
        
        db.session.commit()
        
        session['nombre_usuario'] = usuario.nombre_usuario

        flash("ℹ️¡Tu perfil ha sido actualizado con éxito!", "success")
        return redirect(url_for("usuario.perfil", id=usuario.id))

    form.nombre_usuario.data = usuario.nombre_usuario
    form.correo.data = usuario.correo
    
    return render_template("perfil.html", usuario=usuario, form=form)

# Ruta de logout
@usuario_bp.route("/logout")
@login_requerido
def logout():
    session.clear()
    flash("ℹ️Sesión cerrada", "info")
    return redirect(url_for("usuario.login"))

# Ruta de eliminacion de usuario 
@usuario_bp.route("/perfil/<int:id>/delete", methods=["POST"])
@login_requerido
def delete_perfil(id):
    if id != session.get('id_usuario'):
        flash("No tienes permiso para realizar esta acción.", "danger")
        return redirect(url_for('usuario.perfil', id=session.get('id_usuario')))

    usuario_a_eliminar = Usuario.query.get_or_404(id)
    
    db.session.delete(usuario_a_eliminar)
    db.session.commit()
    
    session.clear()
    
    flash("ℹ️Tu perfil ha sido eliminado con éxito.", "success")
    return redirect(url_for("usuario.login"))