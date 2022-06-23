from myweb import db

class User(db.Model):
    __tablename__ = "USERS"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"