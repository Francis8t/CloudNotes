import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def send_email(name, sender_email, message):
    msg = EmailMessage()
    msg["Subject"] = "New Contact Message - CloudNotes"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_USER")

    msg.set_content(f"""
    New message received:

    Name: {name}
    Email: {sender_email}

    Message:
    {message}
    """)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )
        smtp.send_message(msg)