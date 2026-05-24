from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, abort
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Query

from app import app, db, login_manager
from models import Report, Grade, get_grade
from user import User, get_user, find_by_email, create_user

@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
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
            return redirect(url_for("login", email=email, msg="wrongpwd"))
        login_user(user)

        next = request.args.get("next")
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return abort(400)

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
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        if request.form["grade"] == "":
            grade = None
        else:
            grade = request.form["grade"]
        if password != password_repeat:
            return redirect(url_for("create_account", msg="pwdnomatch", email=email, grade=request.form["grade"]))
        user = create_user(email, password, grade)
        login_user(user)

        next = request.args.get("next")
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return abort(400)

        return redirect(next or url_for("index"))
    
    grades_from_db = db.session.execute(text("SELECT * FROM grades;")).mappings().all()
    return render_template("create_account.html", grade_list=grades_from_db)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        new_grade = request.form["grade"]
        if new_grade == "":
            current_user.grade = None
        else:
            current_user.grade = new_grade
        db.session.commit()
        return redirect(url_for("account"))

    user_grade = get_grade(current_user.grade)
    if user_grade != None:
        grade_name = user_grade.name
    else:
        grade_name = "not set"
    grades_from_db = db.session.execute(text("SELECT * FROM grades;")).mappings().all()
    return render_template("account.html", grade_id=current_user.grade, grade_name=grade_name, grade_list=grades_from_db)

@app.route("/")
def index():
    # Pull all users from database
    users = User.query.all()
    return render_template("index.html", users=users)

def render_reports(query: Query, template: str, view_all: bool = True):
    # Fetch lookup tables for display
    authors = {row['id']: row['email'] for row in db.session.execute(text("SELECT id, email FROM users")).mappings().all()}
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
