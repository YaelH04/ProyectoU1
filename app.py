from flask import Flask
from models.usuario import db
from routes.rutas_usuario import usuario_bp
from routes.rutas_tarea import tarea_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = "super-clave-secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# crea las tablas si no existen
with app.app_context():
    db.create_all()

# registra blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(tarea_bp)

if __name__ == "__main__":
    app.run(debug=True)
