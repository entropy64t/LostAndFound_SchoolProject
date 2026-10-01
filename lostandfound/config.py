import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, "..", ".env"))
load_dotenv(os.path.join(basedir, "..", ".env"), verbose=True)

SECRET_KEY = os.environ["SECRET_KEY"]
SENDER_EMAIL_DOMAIN = os.environ["SENDER_EMAIL_DOMAIN"]
USER_EMAIL_DOMAIN = os.environ["USER_EMAIL_DOMAIN"]

DB_URI = os.environ["DB_URI"]

TIMEZONE = os.environ["TIMEZONE"]

RESEND_API = os.environ["RESEND_API"]

EMAIL_WHITELIST = os.getenv("EMAIL_WHITELIST", "")
