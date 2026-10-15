from datetime import datetime, timezone

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Query

from lostandfound import db
from lostandfound import timezone as org_timezone
from lostandfound.models import (
    Category,
    Colour,
    Grade,
    all_grades,
    Location,
    Report,
    get_category,
    all_categories,
    get_colour,
    all_colours,
    get_location,
    all_locations,
    get_report,
    User,
    get_user,
    all_users
)
from lostandfound.utility.scoring import (
    all_sorted,
    sort_by_score,
    update_scoring_of_report,
)
from ..utility.markdown import parse_markdown

from . import reports_bp


@reports_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        if not current_user.account_verified or not current_user.is_authenticated:
            return redirect(url_for("index"))

        title = request.form["title"]
        if title == "":
            return redirect(url_for("reports.new"))
        report_type = request.form["report-type"]
        if report_type == "":
            return redirect(url_for("reports.new"))
        item_type = request.form["item-type"]
        if item_type == "":
            return redirect(url_for("reports.new"))
        item_color = request.form["item-color"]
        last_seen_str = request.form["last-seen"]
        location_id = request.form["locations"]
        report_content = request.form["report-content"]

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
            item_owner = request.form["item_owner"]
            pickup_location = request.form["pickup_location"]
            if item_owner:
                report.item_owner = item_owner
            if pickup_location:
                report.pickup_location = pickup_location

        db.session.add(report)
        db.session.commit()
        update_scoring_of_report(report)

        return redirect(url_for("reports.report_details", report_id=report.id))

    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))

    locations_from_db = all_locations()
    colours_from_db = all_colours()
    categories_from_db = all_categories()
    grades_from_db = all_grades()
    verified_users = all_users(True)

    return render_template(
        "new.html",
        category_list=categories_from_db,
        colour_list=colours_from_db,
        location_list=locations_from_db,
        user_list=verified_users,
        grade_list=grades_from_db,
    )


def render_reports(query: Query, template: str, view_all: bool = True):
    if not current_user.account_verified or not current_user.is_authenticated:
        return redirect(url_for("index"))

    authors = {user.id: user.public_name() for user in User.query.all()}
    categories = Category.query.order_by(Category.id).all()
    colours = Colour.query.order_by(Colour.id).all()
    locations = {
        location.id: location.location_string() for location in Location.query.all()
    }

    selected_text = request.args.get("text")
    selected_colour = request.args.get("color", type=int)
    selected_item = request.args.get("category", type=int)
    selected_type = request.args.get("type", "").lower()
    selected_owner = request.args.get("item_owner")

    if selected_text:
        query = query.filter(
            or_(
                Report.title.icontains(selected_text, autoescape=True),
                Report.description.icontains(selected_text, autoescape=True),
            )
        )
    if selected_colour is not None:
        query = query.filter_by(colour=selected_colour)
    if selected_item is not None:
        query = query.filter_by(category=selected_item)
    if selected_type in ("lost", "found"):
        query = query.filter_by(report_type=selected_type)
    if (selected_owner is not None) and (selected_owner != "") and (get_user(selected_owner) is not None):
        query = query.filter_by(item_owner=int(selected_owner))
    reports = db.session.scalars(query.order_by(desc(Report.creation_date))).all()

    verified_users = all_users(True)
    return render_template(
        template,
        reports=reports,
        categories=categories,
        colours=colours,
        selected_colour=selected_colour,
        selected_item=selected_item,
        selected_type=selected_type,
        selected_owner=selected_owner,
        selected_text=selected_text,
        view_all=view_all,
        filter=True,
        org_timezone=org_timezone,
        user_list=verified_users
    )


@reports_bp.route("/all")
@login_required
def all():
    report_type = request.args.get("type", "").lower()
    query = select(Report)
    if report_type in ("lost", "found"):
        query = query.filter_by(report_type=report_type)
    return render_reports(query, "all.html")


@reports_bp.route("/lost")
@login_required
def lost():
    return render_reports(
        select(Report).filter_by(report_type="lost"), "lost.html", view_all=False
    )


@reports_bp.route("/your_reports")
@login_required
def your_reports():
    return render_reports(
        select(Report).filter_by(author=current_user.id), "your_reports.html"
    )


@reports_bp.route("/found")
@login_required
def found():
    return render_reports(
        select(Report).filter_by(report_type="found"), "found.html", view_all=False
    )


@reports_bp.route("/report/<report_id>")
@login_required
def report_details(report_id):
    if not current_user.account_verified:
        return redirect(url_for("index"))

    report = get_report(report_id)
    title = report.title
    report_type = report.report_type
    author = report.author_obj.public_name() if report.author else "not set"
    creation_date = report.creation_date.astimezone(org_timezone).strftime(
        "%Y-%m-%d %H:%M"
    )
    category = report.category_obj
    colour = report.colour_obj
    colour_value = report.colour_obj.colour_hex_value or report.colour_obj.name if report.colour else ""
    description = parse_markdown(report.description)

    last_seen_dt: datetime = report.last_seen
    last_seen = last_seen_dt.strftime("%Y-%m-%d %H:%M") if last_seen_dt else ""
    last_seen_location = report.last_seen_location_obj.location_string() if report.last_seen_location else ""

    item_owner = ""
    pickup_location = ""
    if report_type == "found":
        if report.item_owner:
            item_owner = report.item_owner_obj.public_name()
        if report.pickup_location:
            pickup_location = report.pickup_location_obj.location_string()

    authors = {user.id: user.public_name() for user in User.query.all()}
    locations = {
        location.id: location.location_string() for location in Location.query.all()
    }
    score_pairs = sort_by_score(report)

    return render_template(
        "report/index.html",
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
        author_object=report.author_obj,
        report_id=report_id,
        reports=[pair[0] for pair in score_pairs],
        filter=False,
        scores={pair[0]: int(pair[1]) for pair in score_pairs},
        org_timezone=org_timezone,
    )


@reports_bp.route("/report/<report_id>/edit", methods=["GET", "POST"])
@login_required
def edit_report(report_id):
    if not current_user.account_verified:
        return redirect(url_for("index"))

    report = get_report(report_id)
    if request.method == "POST":
        if not current_user.account_verified or not current_user.is_authenticated or report.author_obj != current_user:
            return redirect(url_for("index"))

        title = request.form["title"]
        if title == "":
            return redirect(url_for("reports.edit_report", report_id=report_id))
        item_type = request.form["item-type"]
        if item_type == "":
            return redirect(url_for("reports.edit_report", report_id=report_id))
        item_color = request.form["item-color"]
        last_seen_str = request.form["last-seen"]
        location_id = request.form["locations"]
        report_content = request.form["report-content"]

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
            item_owner = request.form["item_owner"]
            pickup_location = request.form["pickup_location"]
            report.item_owner = item_owner or None
            report.pickup_location = pickup_location or None

        db.session.commit()
        update_scoring_of_report(report)
        return redirect(url_for("reports.report_details", report_id=report_id))

    if report.author_obj != current_user:
        return redirect(url_for("reports.report_details", report_id=report_id))

    title = report.title
    report_type = report.report_type
    author = report.author_obj.public_name() if report.author else "unknown"
    creation_date = report.creation_date.astimezone(org_timezone).strftime(
        "%Y-%m-%d %H:%M"
    )
    category = report.category if report.category else ""
    colour = report.colour if report.colour else ""
    description = report.description
    last_seen_dt: datetime = report.last_seen
    last_seen = last_seen_dt.strftime("%Y-%m-%dT%H:%M") if last_seen_dt else ""
    last_seen_location = report.last_seen_location if report.last_seen_location else ""
    item_owner = report.item_owner if report.report_type != "lost" else ""
    pickup_location = report.pickup_location if report.report_type != "lost" else ""

    locations_from_db = all_locations()
    colours_from_db = all_colours()
    categories_from_db = all_categories()
    grades_from_db = all_grades()
    verified_users = all_users(True)

    return render_template(
        "report/edit.html",
        report_id=report_id,
        title=title,
        report_type=report_type,
        author=author,
        created=creation_date,
        category=category,
        colour=colour,
        description=description,
        last_seen=last_seen,
        last_seen_location=last_seen_location,
        item_owner=item_owner,
        pickup_location=pickup_location,
        category_list=categories_from_db,
        colour_list=colours_from_db,
        grade_list=grades_from_db,
        location_list=locations_from_db,
        user_list=verified_users,
    )


@reports_bp.route("/report/<report_id>/delete", methods=["GET", "POST"])
@login_required
def delete_report(report_id):
    if not current_user.account_verified:
        return redirect(url_for("index"))
    if request.method == "POST":
        report = get_report(report_id)
        if report.author_obj != current_user:
            return redirect(url_for("reports.report_details", report_id=report_id))
        db.session.delete(report)
        db.session.commit()
        return redirect(url_for("index"))
    return redirect(url_for("reports.report_details", report_id=report_id))


@reports_bp.route("/matches")
@login_required
def matches():
    if not current_user.account_verified:
        return redirect(url_for("index"))

    selected_filter = request.args.get("filter")
    selected_order = request.args.get("order")
    all_matches = all_sorted(selected_filter == "mine", selected_order == "created")
    return render_template(
        "matches.html",
        all_matches=all_matches,
        get_report=get_report,
        selected_filter=selected_filter,
        selected_order=selected_order,
    )
