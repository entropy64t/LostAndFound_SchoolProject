from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, select, func, desc, or_
from sqlalchemy.orm import Query

from urllib.parse import urlparse
import secrets
import string

from app import app, db, login_manager, babel, org_timezone
from models import Report, get_report, Grade, get_grade, Category, get_category, Colour, get_colour, Location, get_location
from user import User, get_user, find_by_email, create_user

from verification import send_message_email, send_pwreset, verify_domain

from flask_babel import gettext as lang

from scoring import sort_by_score, update_scoring_of_report, all_sorted

from server_secrets import sender_replyto_address, email_domain

@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    # TODO the color picker from the report filter is more accessible and probably would also fit better on this page
    if request.method == "POST":
        if not current_user.account_verified or not current_user.is_authenticated:
            return redirect(url_for("index"))

        title = request.form['title']
        report_type = request.form['report-type']
        item_type = request.form['item-type']
        item_color = request.form['item-color']
        last_seen_str = request.form['last-seen']
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
            category=item_type if item_type else None,
            colour=item_color if item_color else None,
            creation_date=datetime.now(timezone.utc),
            last_seen=last_seen,
            last_seen_location=location_id if location_id else None,
            description=report_content,
        )

        if report_type != "lost":
            item_owner = request.form['item_owner']
            pickup_location = request.form['pickup_location']
            if item_owner:
                report.item_owner = item_owner
            if pickup_location:
                report.pickup_location = pickup_location
        
        db.session.add(report)
        db.session.commit()
        update_scoring_of_report(report)
        
        return redirect(url_for("all"))

    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))

    
    locations_from_db = Location.query.order_by(Location.id).all()
    colours_from_db = Colour.query.order_by(Colour.id).all()
    categories_from_db = Category.query.order_by(Category.id).all()
    grades_from_db = Grade.query.order_by(Grade.id).all()
    verified_users = db.session.scalars(select(User).filter_by(account_verified=True).order_by(User.grade)).all()
    
    return render_template("new.html", 
                           category_list=categories_from_db, 
                           colour_list=colours_from_db, 
                           location_list=locations_from_db, 
                           user_list=verified_users,
                           grade_list=grades_from_db)

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

@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == "POST":
        receiver_address = request.form["email"]
        user = find_by_email(receiver_address)
        if user != None:
            otp_plaintext = ""
            for i in range(16): # OTP length
                otp_plaintext += secrets.choice(string.digits + string.ascii_letters)
            pw_reset_url = url_for("check_pwreset", otp=otp_plaintext, email=receiver_address, _external=True)
            user.set_pwreset(otp_plaintext)
            db.session.commit()
            send_pwreset(receiver_address, pw_reset_url)
        return redirect(url_for("reset_password", msg="sent"))

    return render_template("pwreset/index.html")

@app.route('/reset/link', methods=['GET', 'POST'])
def check_pwreset():
    if request.method == "POST":
        email = request.args.get("email")
        otp = request.args.get("otp")
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        if password != password_repeat:
            return redirect(url_for("check_pwreset", msg="pwdnomatch", email=email, otp=otp))
        user = find_by_email(email)
        if user == None:
            return redirect(url_for("reset_password"))
        if not user.check_pwreset(otp):
            return redirect(url_for("reset_password", msg="wrongotp"))
        user.set_password(password)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))

    return render_template("pwreset/check.html")

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
    
    grades_from_db = Grade.query.all()
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
    return render_template("verification/index.html", prefill=prefill, email_domain=email_domain)

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
    return render_template("account/index.html", grade_id=current_user.grade, grade_name=grade_name, grade_list=grades_from_db)

@app.route("/account/delete", methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == "POST":
        password = request.form["password"]
        if not current_user.check_password(password):
            return redirect(url_for("delete_account", msg="wrongpwd"))
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("account/delete.html")

@app.route("/")
@login_required
def index():
    if not current_user.account_verified:
        return redirect(url_for("verify_account"))

    total_reports = db.session.scalar(select(func.count(Report.id)))
    lost_reports = db.session.scalar(select(func.count(Report.id)).where(Report.report_type=="lost"))
    found_reports = db.session.scalar(select(func.count(Report.id)).where(Report.report_type=="found"))

    return render_template("index.html", total_reports=total_reports, lost_reports=lost_reports, found_reports=found_reports, sender_replyto_address=sender_replyto_address)

@app.route('/setlang/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang

    # stay on current page
    return redirect(request.referrer or url_for('home'))

def render_reports(query: Query, template: str, view_all: bool = True):
    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))

    # Fetch lookup tables for display
    authors = {u.id: u.public_name() for u in User.query.all()}
    categories = Category.query.order_by(Category.id).all()
    colours = Colour.query.order_by(Colour.id).all()
    locations = {l.id: l.location_string() for l in Location.query.all()}
    
    selected_text = request.args.get('text')
    selected_colour = request.args.get('color', type=int)
    selected_item = request.args.get('category', type=int)
    selected_type = request.args.get('type', "").lower()
    selected_owner = request.args.get('item_owner')
    
    if selected_text:
        query = query.filter(or_(Report.title.icontains(selected_text, autoescape=True), Report.description.icontains(selected_text, autoescape=True))) # icontains is case-insensitive contains
    if selected_colour is not None:
        query = query.filter_by(colour=selected_colour)
    if selected_item is not None:
        query = query.filter_by(category=selected_item)
    if selected_type in ("lost", "found"):
        query = query.filter_by(report_type=selected_type)
    if selected_owner == "me":
        query = query.filter_by(item_owner=current_user.id)
    reports = query.order_by(desc(Report.creation_date)).all()
    
    return render_template(
        template,
        reports=reports,
        authors=authors,
        categories=categories,
        colours=colours,
        selected_colour=selected_colour,
        selected_item=selected_item,
        selected_type=selected_type,
        selected_owner=selected_owner,
        selected_text=selected_text,
        locations=locations,
        view_all=view_all,
        get_category=get_category,
        get_colour=get_colour,
        get_location=get_location,
        get_user=get_user,
        filter=True,
        org_timezone=org_timezone
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

@app.route("/report/<report_id>")
@login_required
def report_details(report_id):
    if not current_user.account_verified:
        return redirect(url_for("index"))

    report = get_report(report_id)
    print(report)

    title = report.title

    report_type = report.report_type
    author = get_user(report.author).public_name() if report.author else "not set"

    creation_date = report.creation_date.astimezone(org_timezone).strftime('%Y-%m-%d %H:%M')

    category = get_category(report.category)
    colour = get_colour(report.colour)
    colour_value = get_colour(report.colour).colour_value or get_colour(report.colour).name if report.colour else ""
    description = report.description
    
    # TODO Images
    
    last_seen_dt: datetime = report.last_seen
    last_seen = ""
    if last_seen_dt:
        last_seen = last_seen_dt.strftime('%Y-%m-%d %H:%M')
    last_seen_location = get_location(report.last_seen_location).location_string() if report.last_seen_location else ""

    item_owner = ""
    pickup_location = ""
    if report_type == "found":
        if report.item_owner:
            item_owner = get_user(report.item_owner).public_name()
        if report.pickup_location:
            pickup_location = get_location(report.pickup_location).location_string()
            
    all_reports = Report.query.all()
    authors = {u.id: u.public_name() for u in User.query.all()}
    locations = {l.id: l.location_string() for l in Location.query.all()}
    score_pairs = sort_by_score(report)
    
    return render_template("report/index.html", 
                           report_type=report_type, 
                           title=title, 
                           created=creation_date, 
                           author=author,
                           category=category, 
                           colour=colour, 
                           colour_value=colour_value,
                           description=description, 
                           last_seen=last_seen, 
                           last_seen_location=last_seen_location, 
                           item_owner=item_owner, 
                           pickup_location=pickup_location, 
                           author_object=get_user(report.author), 
                           report_id=report_id,
                           reports=[pair[0] for pair in score_pairs],
                           authors=authors,
                           locations=locations,
                           filter=False,
                           scores={pair[0]: int(pair[1]) for pair in score_pairs},
                           get_category=get_category, 
                           get_colour=get_colour, 
                           get_location=get_location,
                           get_user=get_user,
                           org_timezone=org_timezone
                           )

@app.route("/report/<report_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    # TODO the color picker from the report filter is more accessible and probably would also fit better on this page
    if not current_user.account_verified:
        return redirect(url_for("index"))

    report = get_report(report_id)
    
    if request.method == "POST":
        if not current_user.account_verified or not current_user.is_authenticated or get_user(report.author) != current_user:
            return redirect(url_for("index"))
        
        title = request.form['title']
        item_type = request.form['item-type']
        item_color = request.form['item-color']
        last_seen_str = request.form['last-seen']
        location_id = request.form['locations']
        report_content = request.form['report-content']

        last_seen = None
        if last_seen_str:
            try:
                last_seen = datetime.fromisoformat(last_seen_str)
            except ValueError:
                last_seen = None

        report.title = title
        report.category = item_type if item_type else None
        report.colour = item_color if item_color else None
        report.last_seen = last_seen
        report.last_seen_location = location_id if location_id else None
        report.description = report_content
        
        if report.report_type != "lost":
            item_owner = request.form['item_owner']
            pickup_location = request.form['pickup_location']
            if item_owner:
                report.item_owner = item_owner
            else:
                report.item_owner = None
            if pickup_location:
                report.pickup_location = pickup_location
            else:
                report.pickup_location = None

        db.session.commit()
        update_scoring_of_report(report)

        return redirect(url_for("report_details", report_id=report_id))

    if get_user(report.author) != current_user:
        return redirect(url_for("report_details", report_id=report_id))

    title = report.title

    report_type = report.report_type
    author = get_user(report.author).public_name() if report.author else "unknown"

    creation_date = report.creation_date.astimezone(org_timezone).strftime('%Y-%m-%d %H:%M')

    category = get_category(report.category).id if report.category else ""
    colour = get_colour(report.colour).id if report.colour else ""
    description = report.description
    
    last_seen_dt: datetime = report.last_seen
    last_seen = ""
    if last_seen_dt:
        last_seen = last_seen_dt.strftime("%Y-%m-%dT%H:%M")
    last_seen_location = get_location(report.last_seen_location).id if report.last_seen_location else ""
   
    item_owner = ""
    pickup_location = ""
    if report_type != "lost":
        item_owner = report.item_owner
        pickup_location = report.pickup_location
   
    # Get option lists from db
    locations_from_db = Location.query.order_by(Location.id).all()
    colours_from_db = Colour.query.order_by(Colour.id).all()
    categories_from_db = Category.query.order_by(Category.id).all()
    verified_users = db.session.scalars(select(User).filter_by(account_verified=True).order_by(User.grade)).all()

    return render_template("report/edit.html", report_id=report_id, title=title, report_type=report_type, author=author, created=creation_date, category=category, colour=colour, description=description,
                           last_seen=last_seen, last_seen_location=last_seen_location, item_owner=item_owner, pickup_location=pickup_location,
                           category_list=categories_from_db, colour_list=colours_from_db, location_list=locations_from_db, user_list=verified_users)

@app.route("/report/<report_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_report(report_id):
    if not current_user.account_verified:
        return redirect(url_for("index"))
    if request.method == "POST":
        report = get_report(report_id)
        if get_user(report.author) != current_user:
            return redirect(url_for("report_details", report_id=report_id))
        db.session.delete(report)
        db.session.commit()
        return redirect(url_for("index"))
    return redirect(url_for("report_details", report_id=report_id))

@app.route("/matches")
@login_required
def matches():
    if not current_user.account_verified:
        return redirect(url_for("index"))

    selected_filter = request.args.get('filter')
    selected_order = request.args.get('order')

    all_matches = all_sorted(selected_filter == "mine", selected_order == "created")
    return render_template("matches.html", all_matches=all_matches, get_report=get_report, selected_filter=selected_filter, selected_order=selected_order)

@login_manager.user_loader
def load_user(user_id: str):
    return get_user(user_id)
