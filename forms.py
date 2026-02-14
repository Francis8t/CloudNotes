from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(), Length(min=3, max=150)
    ])
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password")
    ])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")
    
class NoteForm(FlaskForm):
    content = TextAreaField("Your Note", validators=[
        DataRequired(), Length(min=3)
    ])
    submit = SubmitField("Save Note")
    

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Send Message")