from flask import Flask, render_template, request, redirect, url_for, abort, session
from markupsafe import escape
from flask_login import LoginManager, login_required, login_user, logout_user
from zoneinfo import ZoneInfo

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_babel import Babel, gettext as lang

from server_secrets import secret_key, default, db_localhost

import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secret_key)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Database connection init
DB_URL = os.getenv("DATABASE_URL", default) 
DB_URL = db_localhost
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

db = SQLAlchemy(app)

# babel config
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pl']
app.jinja_env.globals['lang'] = lang
def get_locale():
    return session.get('lang', 'en')
babel = Babel(app, locale_selector=get_locale)

# timezone 
org_timezone = ZoneInfo("Europe/Warsaw")

import routes, models, user

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # for production
