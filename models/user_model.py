from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default="user")

    def __init__(self, name: str, email: str, password: str, role: str = "user"):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def verify_password(self, password):
        return check_password_hash(self.password, password)

