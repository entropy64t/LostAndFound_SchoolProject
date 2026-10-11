import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, "..", ".env"))
load_dotenv(os.path.join(basedir, "..", ".env"), verbose=True)

# Flask application
TIMEZONE = os.environ["TIMEZONE"]
DB_URI = os.environ["DB_URI"]
SECRET_KEY = os.environ["SECRET_KEY"]

# Email sending
RESEND_API = os.environ["RESEND_API"]
SENDER_EMAIL_DOMAIN = os.environ["SENDER_EMAIL_DOMAIN"]
# Fallback email sending
FALLBACK_SENDER_ADDRESS = os.environ["FALLBACK_SENDER_ADDRESS"]
FALLBACK_SENDER_PASSWORD = os.environ["FALLBACK_SENDER_PASSWORD"]

# User email domain verification
USER_EMAIL_DOMAIN = os.environ["USER_EMAIL_DOMAIN"]
EMAIL_WHITELIST = os.getenv("EMAIL_WHITELIST", "")
