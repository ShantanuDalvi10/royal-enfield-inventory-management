import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///inventory.db"


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REGISTRATION_PIN = os.environ.get("REGISTRATION_PIN")
