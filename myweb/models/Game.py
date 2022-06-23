from random import random
from myweb import db

class Game(db.Model):
    __tablename__ = "PARTIDAS"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'), nullable=False)
    intentos = db.Column(db.Integer, nullable=False)
    random = db.Column(db.String(20))
    duracion = db.Column(db.String(20))
    estado = db.Column(db.String(20))
    fecha = db.Column(db.DateTime)

    def __init__(self, user_id, intentos, random, duracion, estado, fecha):
        self.user_id = user_id
        self.intentos = intentos
        self.random = random
        self.duracion = duracion
        self.estado = estado
        self.fecha = fecha
    
    def __repr__(self) -> str:
        return f"<Game {self.id}>"