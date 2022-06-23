class Config:
    DEBUG=True
    TESTING=True
    #Configuracion de la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/flask_db'

class ProductionConfig(Config):
    DEBUG=False
    TESTING=False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/flask_db'

class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    DEBUG=True
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/flask_db'