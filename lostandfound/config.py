import os

from dotenv import load_dotenv

"""
sender_address = os.getenv("SENDER_ADDRESS", "lost.and.found.vlo@gmail.com")
sender_password = os.getenv("SENDER_PASSWORD", "xqfs upls kiyz izvi")
sender_replyto_address = os.getenv("REPLYTO_ADDRESS", "lost.and.found.vlo@gmail.com")
secret_key = "4d3786b49efdbe8c45dfeaab9804597c69da20d7400745afe13d028a984036d0"
email_domain = "v-lo.krakow.pl"

default = "postgresql://postgres:postgres291830@host.docker.internal:5432/LostAndFound"
db_localhost = "postgresql://postgres:postgres291830@localhost:5432/LostAndFound"
"""

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, "..", ".env"))
load_dotenv(os.path.join(basedir, "..", ".env"), verbose=True)

SECRET_KEY = os.environ["SECRET_KEY"]
SENDER_EMAIL_DOMAIN = os.environ["SENDER_EMAIL_DOMAIN"]
USER_EMAIL_DOMAIN = os.environ["USER_EMAIL_DOMAIN"]

DB_URI = os.environ["DB_URI"]

TIMEZONE = os.environ["TIMEZONE"]
