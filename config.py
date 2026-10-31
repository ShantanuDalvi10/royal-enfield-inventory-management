import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = "sqlite:///inventory.db"


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REGISTRATION_PIN = os.environ.get("REGISTRATION_PIN")
