from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm, ContactForm
import requests
import os
from dotenv import load_dotenv
from email_utils import send_email




load_dotenv() # Load environment variables from .env file

def fetch_tech_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "technology",
        "language": "en",
        "apiKey": os.getenv("NEWS_API_KEY")
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("articles", [])[:5]
    except Exception:
        return []




login_manager = LoginManager()
login_manager.login_view = "login"


#App factory pattern to create the Flask application instance and initialize extensions. This allows for better modularity and testing.
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Create the Flask application instance using the factory function. This instance will be used to run the application and handle requests.
app = create_app()


# Index route to render the homepage. This is a simple route that serves as the landing page for the application.
@app.route("/")
def index():
    return render_template("index.html")

#Registration route to handle new user sign-ups. It checks if the user is already logged in, validates the registration form, and creates a new user account if the form is valid. If the email is already registered, it flashes an error message.
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

#Login route to handle user authentication. It checks if the user is already logged in, validates the login form, and logs the user in if the credentials are correct. If the credentials are invalid, it flashes an error message.
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("login.html", form=form)


#Logout route to handle user logout. It requires the user to be logged in and logs them out, then flashes a success message and redirects to the homepage.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

#Dashboard route to display the user's notes and fetch technology news. It requires the user to be logged in, handles note creation through a form, and displays the user's existing notes along with the latest technology news articles.
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = NoteForm()

    if form.validate_on_submit():
        note = Note(
            content=form.content.data,
            author=current_user
        )
        db.session.add(note)
        db.session.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for("dashboard"))

    notes = current_user.notes
    articles = fetch_tech_news()

    return render_template(
        "dashboard.html",
        form=form,
        notes=notes,
        articles=articles
    )

#Delete note route to handle the deletion of user notes. It requires the user to be logged in, checks if the note belongs to the current user or if the user is an admin, and deletes the note if authorized. If the user is not authorized to delete the note, it returns a 403 error.
@app.route("/delete_note/<int:note_id>")
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.author != current_user and not current_user.is_admin:
        abort(403)

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("dashboard"))



@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        send_email(
            form.name.data,
            form.email.data,
            form.message.data
        )
        flash("Message sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    notes = Note.query.all()

    return render_template("admin.html", users=users, notes=notes)


if __name__ == "__main__":
    app.run(debug=True)