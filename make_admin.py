# This script promotes a user to admin status. Run it once after creating the user.

from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(email="test@test.com").first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("User promoted to admin.")
    else:
        print("User not found.")
