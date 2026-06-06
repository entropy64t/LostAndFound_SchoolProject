from flask import Flask, render_template, request, redirect, url_for, abort, session
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_babel import Babel, gettext as lang

app = Flask(__name__)
app.secret_key = "Bda4L_rbDg2nMbE0Z3ZALk-zK2ODy5eCXyAfTCObtjg"
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Database connection init
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres291830@localhost/LostAndFound" # TODO Update database hostname for production environment TODO store secrets separately
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
    app.run(debug=True) # TODO change for production
