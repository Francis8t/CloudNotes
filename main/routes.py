from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm, ContactForm
import requests
import os
from dotenv import load_dotenv
from email_utils import send_email
from . import main



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



# Index route to render the homepage. This is a simple route that serves as the landing page for the application.
@main.route("/")
def index():
    return render_template("index.html")



#Dashboard route to display the user's notes and fetch technology news. It requires the user to be logged in, handles note creation through a form, and displays the user's existing notes along with the latest technology news articles.
@main.route("/dashboard", methods=["GET", "POST"])
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
        return redirect(url_for("main.dashboard"))

    notes = current_user.notes
    articles = fetch_tech_news()

    return render_template(
        "dashboard.html",
        form=form,
        notes=notes,
        articles=articles
    )

#Delete note route to handle the deletion of user notes. It requires the user to be logged in, checks if the note belongs to the current user or if the user is an admin, and deletes the note if authorized. If the user is not authorized to delete the note, it returns a 403 error.
@main.route("/delete_note/<int:note_id>")
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.author != current_user and not current_user.is_admin:
        abort(403)

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("main.dashboard"))



@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        send_email(
            form.name.data,
            form.email.data,
            form.message.data
        )
        flash("Message sent successfully!", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form=form)


