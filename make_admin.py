from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(email="test3434@test.com").first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("User promoted to admin.")
    else:
        print("User not found.")
