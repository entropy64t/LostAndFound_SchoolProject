from flask import (
    Flask,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import func, select

from lostandfound import db, login
from lostandfound.email.email_config import CONTACT_ADDRESS
from lostandfound.models import Report
from lostandfound.user import get_user


@login_required
def index():
    if not current_user.account_verified:
        return redirect(url_for("auth.verify_account"))

    total_reports = db.session.scalar(select(func.count(Report.id)))
    lost_reports = db.session.scalar(
        select(func.count(Report.id)).where(Report.report_type == "lost")
    )
    found_reports = db.session.scalar(
        select(func.count(Report.id)).where(Report.report_type == "found")
    )

    return render_template(
        "index.html",
        total_reports=total_reports,
        lost_reports=lost_reports,
        found_reports=found_reports,
        sender_replyto_address=CONTACT_ADDRESS,
    )


def set_language(lang):
    if lang in current_app.config["BABEL_SUPPORTED_LOCALES"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("index"))


def load_user(user_id: str):
    return get_user(int(user_id))


def register_routes(app: Flask):
    app.add_url_rule("/", endpoint="index", view_func=index)
    app.add_url_rule("/setlang/<lang>", endpoint="set_language", view_func=set_language)
    login.user_loader(load_user)
