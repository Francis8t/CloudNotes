from flask import abort, render_template
from flask_login import login_required, current_user
from models import User, Note
from . import admin



@admin.route("/admin")
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    notes = Note.query.all()

    return render_template("admin.html", users=users, notes=notes)