from zoneinfo import ZoneInfo

import resend
from flask import Flask, session
from flask_babel import Babel
from flask_babel import gettext as lang
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from lostandfound.config import DB_URI, RESEND_API, SECRET_KEY, TIMEZONE

# Database, flask-login and babel init
db = SQLAlchemy()
babel = Babel()
login = LoginManager()

# timezone
timezone = ZoneInfo(TIMEZONE)
resend.api_key = RESEND_API


def create_app():
    from lostandfound.account import account_bp
    from lostandfound.auth import auth_bp
    from lostandfound.reports import reports_bp

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    # babel config
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "pl"]
    app.jinja_env.globals["lang"] = lang

    db.init_app(app)
    login.init_app(app)
    login.login_view = "auth.login"
    babel.init_app(app, locale_selector=lambda: session.get("lang", "en"))

    app.register_blueprint(account_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reports_bp)

    from lostandfound import routes

    routes.register_routes(app)

    app.secret_key = SECRET_KEY

    return app
