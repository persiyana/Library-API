from api import app, db
from models.user_model import UserModel
from werkzeug.security import generate_password_hash

def create_admin_user():
    admin_email = "admin@gmail.com"
    existing_admin = UserModel.query.filter_by(email=admin_email).first()

    if not existing_admin:
        admin_user = UserModel(
            name="Admin",
            email=admin_email,
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
    else:
        print("Admin user already exists.")

with app.app_context():
    db.create_all()
    create_admin_user()