from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")



SECRET_AUTH = os.environ.get("SECRET_AUTH")

MEDIA_PATH = 'media/'

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

BASE_URL = os.environ.get("BASE_URL")
