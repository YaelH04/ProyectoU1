from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column("usuario", db.String(50), nullable=False, unique=True)
    correo = db.Column("email", db.String(120), nullable=False, unique=True)
    contraseña_hash = db.Column("password", db.String(128), nullable=False)

    tareas = db.relationship(
        "Tarea", 
        backref="propietario", 
        lazy=True, 
        cascade="all, delete-orphan"
    )

    def set_contraseña(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    def check_contraseña(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)