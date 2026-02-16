import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file


class Config:
    SECRET_KEY = os.getenv("MY_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("MY_DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False