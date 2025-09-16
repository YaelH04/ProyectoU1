from models.usuario import db

class Tarea(db.Model):
    __tablename__ = "tareas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column("titulo", db.String(100), nullable=False)
    descripcion = db.Column("descripcion", db.Text)
    estado = db.Column("estado", db.Boolean, default=False)  # False = pendiente
    id_usuario = db.Column("id_usuario", db.Integer, db.ForeignKey("usuarios.id"), nullable=False)