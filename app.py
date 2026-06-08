from flask import Flask, render_template, request, redirect, url_for, abort, session
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_babel import Babel, gettext as lang

from server_secrets import secret_key

import os

app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Database connection init
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres291830@host.docker.internal:5432/LostAndFound")
# DB_URL = "postgresql://postgres:postgres291830@localhost:5432/LostAndFound" # for local testing
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
#"postgresql://postgres:postgres291830@host.docker.internal:5432/LostAndFound" # TODO Update database hostname for production environment TODO store secrets separately
db = SQLAlchemy(app)

# babel config
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pl']
app.jinja_env.globals['lang'] = lang

def get_locale():
    return session.get('lang', 'en')
babel = Babel(app, locale_selector=get_locale)

import routes, models, user

if __name__ == "__main__":
    # app.run(debug=True) # for local testing
    app.run(host="0.0.0.0", port=5000) # for production
