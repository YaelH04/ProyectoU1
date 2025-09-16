class Config:
    SECRET_KEY = "super-clave-secreta"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:micontraseña@localhost/miniproyecto"
    SQLALCHEMY_TRACK_MODIFICATIONS = False