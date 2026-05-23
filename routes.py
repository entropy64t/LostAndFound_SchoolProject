from flask import Blueprint, render_template, request, redirect, url_for, abort
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Query

from app import app, db, login_manager
from models import Report
from user import User, get_user, find_by_email, create_user

@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        title = request.form['title']
        report_type = request.form['report-type']
        item_type = request.form['item-type']
        item_color = request.form['item-color']
        location_id = request.form['locations']
        report_content = request.form['report-content']
        author = current_user.id
        
        report = Report(
            author=author,
            title=title,
            report_type=report_type,
            category=int(item_type),
            colour=int(item_color),
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
            return redirect(url_for("index"))
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
        if password != password_repeat:
            return render_template("create_account.html")
        user = create_user(email, password)
        login_user(user)

        next = request.args.get("next")
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return abort(400)

        return redirect(next or url_for("index"))
    return render_template("create_account.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html")

@app.route("/")
def index():
    # Pull all users from database
    users = User.query.all()
    return render_template("index.html", users=users)

def render_reports(query: Query, template: str):
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
    return render_reports(query, "lost.html")

@app.route("/found")
@login_required
def found():
    query = Report.query.filter_by(report_type="found")
    return render_reports(query, "found.html")

@login_manager.user_loader
def load_user(user_id: str):
    return get_user(user_id)
