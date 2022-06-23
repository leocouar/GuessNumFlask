from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app= Flask(__name__)

#cargar configuracion de la db
app.config.from_object('config.DevelopmentConfig')

#crear instancia de la base de datos
db=SQLAlchemy(app)

#importar Vistas
#vistas de usuarios
from myweb.views.userView import userView
app.register_blueprint(userView)
#vistas de juegos
from myweb.views.gameView import gameView
app.register_blueprint(gameView)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

