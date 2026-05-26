from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, abort
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Query

from urllib.parse import urlparse
import secrets
import string

from app import app, db, login_manager
from models import Report, Grade, get_grade
from user import User, get_user, find_by_email, create_user

from verification import send_message_email, verify_domain

@app.route("/new", methods=["GET", "POST"])
@login_required
def new(): # TODO make sure the user is logged in and verified - also for POST request
    if request.method == "POST":
        if not current_user.account_verified or not current_user.is_authenticated:
            return redirect(url_for("index"))

        title = request.form['title']
        report_type = request.form['report-type']
        item_type = request.form['item-type']
        item_color = request.form['item-color']
        last_seen_str = request.form.get('last-seen')
        location_id = request.form['locations']
        report_content = request.form['report-content']
        author = current_user.id

        last_seen = None
        if last_seen_str:
            try:
                last_seen = datetime.fromisoformat(last_seen_str)
            except ValueError:
                last_seen = None

        report = Report(
            author=author,
            title=title,
            report_type=report_type,
            category=int(item_type),
            colour=int(item_color),
            creation_date=datetime.now(timezone.utc),
            last_seen=last_seen,
            last_seen_location=int(location_id),
            description=report_content,
        )
        
        db.session.add(report)
        db.session.commit()
        
        return redirect(url_for("all"))

    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))
    locations_from_db = db.session.execute(text("SELECT * FROM locations;")).mappings().all()
    colours_from_db = db.session.execute(text("SELECT * FROM colours;")).mappings().all()
    categories_from_db = db.session.execute(text("SELECT * FROM categories;")).mappings().all()

    return render_template("new.html", category_list=categories_from_db, colour_list=colours_from_db, location_list=locations_from_db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = find_by_email(email)
        if user is None:
            # user does not exist
            return redirect(url_for("create_account", email=email, next=request.args.get("next")))
        if not user.check_password(password):
            return redirect(url_for("login", email=email, msg="wrongpwd", next=request.args.get("next")))
        login_user(user)

        next = request.args.get("next")
        if next:
            if urlparse(next).netloc:
                return abort(400)

        return redirect(next or url_for("index"))
    return render_template("login.html")

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form["email"]
        display_name = request.form["display_name"]
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        if request.form["grade"] == "":
            grade = None
        else:
            grade = request.form["grade"]
        if password != password_repeat:
            return redirect(url_for("create_account", msg="pwdnomatch", email=email, grade=request.form["grade"], display_name=display_name, next=request.args.get("next")))

        if find_by_email(email) != None:
            return redirect(url_for("create_account", msg="existent", email=email, grade=request.form["grade"], display_name=display_name, next=request.args.get("next")))
        user = create_user(email, display_name, password, grade)
        login_user(user)

        next = request.args.get("next")
        if next:
            if urlparse(next).netloc:
                return abort(400)

        return redirect(next or url_for("index"))
    
    grades_from_db = db.session.execute(text("SELECT * FROM grades;")).mappings().all()
    return render_template("create_account.html", grade_list=grades_from_db)

@app.route("/verification/", methods=["GET", "POST"])
@login_required
def verify_account():
    if request.method == "POST":
        receiver_address = request.form["verif_mail"]
        if not verify_domain(receiver_address):
            return redirect(url_for("verify_account", msg="wrongdomain"))
        otp_plaintext = ""
        for i in range(6): # OTP length
            otp_plaintext += secrets.choice(string.digits)
        current_user.set_otp(otp_plaintext)
        db.session.commit()
        send_message_email(receiver_address, otp_plaintext, current_user.email, current_user.display_name)
        return redirect(url_for("check_verification"))


    if verify_domain(current_user.email):
        prefill = current_user.email
    else:
        prefill = ""
    return render_template("verification/index.html", prefill=prefill)

@app.route("/verification/check", methods=["GET", "POST"])
@login_required
def check_verification():
    if request.method == "POST":
        received_otp = request.form["otp"]
        if not current_user.check_otp(received_otp):
            return redirect(url_for("check_verification", msg="wrongotp"))

        current_user.account_verified = True
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("verification/check.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        new_grade = request.form["grade"]
        if new_grade == "":
            current_user.grade = None
        else:
            current_user.grade = new_grade
        new_name = request.form["display_name"]
        current_user.display_name = new_name
        db.session.commit()

        new_password = request.form["new_password"]
        if new_password != "":
            new_password_repeat = request.form["new_password-repeat"]
            if new_password == new_password_repeat:
                old_password = request.form["password"]
                if current_user.check_password(old_password):
                    current_user.set_password(new_password)
                    db.session.commit()
                else:
                    return redirect(url_for("account", msg="wrongpwd"))
            else:
                return redirect(url_for("account", msg="pwdnomatch"))

        new_email = request.form["new_email"]
        if new_email != "":
            new_email_repeat = request.form["new_email-repeat"]
            if new_email == new_email_repeat:
                current_user.email = new_email
                db.session.commit()
            else:
                return redirect(url_for("account", email_msg="emailnomatch"))
    
        return redirect(url_for("account"))

    user_grade = get_grade(current_user.grade)
    if user_grade != None:
        grade_name = user_grade.name
    else:
        grade_name = "not set"
    grades_from_db = db.session.execute(text("SELECT * FROM grades;")).mappings().all()
    return render_template("account.html", grade_id=current_user.grade, grade_name=grade_name, grade_list=grades_from_db)

    # TODO Separate page for account deletion?

@app.route("/")
@login_required
def index():
    # Pull all users from database
    users = User.query.all()
    return render_template("index.html", users=users)

def render_reports(query: Query, template: str, view_all: bool = True): # TODO make sure the user is logged in and verified - also for POST request
    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))

    # Fetch lookup tables for display
    authors = {row['id']: row['display_name'] for row in db.session.execute(text("SELECT id, display_name FROM users")).mappings().all()}
    categories = {row['id']: row['name'] for row in db.session.execute(text("SELECT id, name FROM categories;")).mappings().all()}
    colours = {
        row['id']: {
            'name': row['name'],
            'display_name': row['display_name'],
            'value': row.get('colour_value') or row['name']
        }
        for row in db.session.execute(text("SELECT id, name, display_name, colour_value FROM colours;")).mappings().all()
    }
    locations = {row['id']: (row['building_level'], row['name']) for row in db.session.execute(text("SELECT id, name, building_level FROM locations;")).mappings().all()}
    
    selected_colour = request.args.get('color', type=int)
    selected_item = request.args.get('category', type=int)
    selected_type = request.args.get('type', "").lower()
    
    if selected_colour is not None:
        query = query.filter_by(colour=selected_colour)
    if selected_item is not None:
        query = query.filter_by(category=selected_item)
    if selected_type in ("lost", "found"):
        query = query.filter_by(report_type=selected_type)
    reports = query.all()
    
    return render_template(
        template,
        reports=reports,
        authors=authors,
        categories=categories,
        colours=colours,
        selected_colour=selected_colour,
        selected_item=selected_item,
        selected_type=selected_type,
        locations=locations,
        view_all=view_all
    )

@app.route("/all")
@login_required
def all():
    report_type = request.args.get("type", "").lower()

    query = Report.query
    if report_type in ("lost", "found"):
        query = query.filter_by(report_type=report_type)

    return render_reports(query, "all.html")

@app.route("/lost")
@login_required
def lost():
    query = Report.query.filter_by(report_type="lost")
    return render_reports(query, "lost.html", view_all=False)

@app.route("/your_reports")
@login_required
def your_reports():
    query = Report.query.filter_by(author=current_user.id)
    return render_reports(query, "your_reports.html")

@app.route("/found")
@login_required
def found():
    query = Report.query.filter_by(report_type="found")
    return render_reports(query, "found.html", view_all=False)

@login_manager.user_loader
def load_user(user_id: str):
    return get_user(user_id)
