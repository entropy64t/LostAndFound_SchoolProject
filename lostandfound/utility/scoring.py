import threading
from datetime import datetime, timezone

from coloraide import Color
from flask import Flask, current_app
from flask_login import current_user
from rapidfuzz import fuzz
from sqlalchemy import delete, select, or_

from lostandfound import timezone as org_timezone
from lostandfound import db
from lostandfound.models import Grade, Category, Colour, Location, User, Report, Match, all_reports, get_location, get_colour

_MAX_DELTA_E_VALUE = 20


def _colour_similarity(a: Colour, b: Colour):
    if not a or not b:
        return 0
    c1 = Color(a.colour_hex_value).convert("lab")
    c2 = Color(b.colour_hex_value).convert("lab")

    distance = c1.delta_e(c2, method="2000")

    # 0 = identical, larger = more different
    return max(_MAX_DELTA_E_VALUE - distance, 0)


def score_single(target: Report, item: Report) -> int:
    """Score `item` against `target` on a [0, 100] scale
    - `target` == `item` => 0
    - `target` and `item` have the same report type => 0
    - `target` and `item` have different item category => 0
    - Delta E distance for colour comparison
    - same `location` => 20
    - same `location.level` => 10
    - different locations => 0
    - keywords in title match => [0-25]

    - total: 0 - 65
    """
    if target == item:
        return 0
    if target.report_type == item.report_type:
        return 0
    if target.category != item.category:
        return 0

    colour_score = _colour_similarity(get_colour(target.colour), get_colour(item.colour))

    loc_score = 0
    target_loc = get_location(target.last_seen_location)
    item_loc = get_location(item.last_seen_location)
    if target_loc != None and item_loc != None:
        if target_loc == item_loc:
            loc_score = 20
        elif target_loc.building_level == item_loc.building_level:
            loc_score = 10

    ownership_score = 0
    if target.item_owner and item.author and target.item_owner == item.author:
        ownership_score = 30
    if item.item_owner and target.author and item.item_owner == target.author:
        ownership_score = 30

    title_score = 0
    if target.title and item.title:
        title_score = round(
            fuzz.token_set_ratio(target.title.lower(), item.title.lower()) * 0.3
        )  # toke_set_ration returns [0, 100], so to make the title not have a very large impact scale it down by 5

    return colour_score + loc_score + ownership_score + title_score


def score_against(target: Report, items: list[Report]) -> dict[Report, int]:
    """Score `items` against `target`. For criteria look at `score_single`"""

    return {item: score_single(target, item) for item in items}


# TODO remove the type ignores


def scoring_service(ctx, root: Report, report_list: list[Report], app: Flask):
    with ctx:
        scoring_result = score_against(root, report_list)

        db.session.execute(
            delete(Match).where(
                or_(Match.lost_item == root.id, Match.found_item == root.id)
            )
        )

        db.session.commit()
        for pair in scoring_result:
            if scoring_result[pair] >= 10:  # scoring threshold
                if root.report_type == "lost":
                    lost_item_id = root.id
                    found_item_id = pair.id
                else:
                    lost_item_id = pair.id
                    found_item_id = root.id

                mat = Match(
                    lost_item=lost_item_id,  # type: ignore
                    found_item=found_item_id,  # type: ignore
                    score=scoring_result[pair],  # type: ignore
                    creation_date=datetime.now(timezone.utc),  # type: ignore
                )
                db.session.add(mat)
        db.session.commit()
        db.session.remove()


def update_scoring_of_report(root: Report):
    report_list = all_reports()
    thread = threading.Thread(target=scoring_service, daemon=True, args=(current_app.app_context(), root, report_list, current_app._get_current_object()))
    thread.start()


def sort_by_score(target: Report) -> list[tuple[Report, int]]:
    if target.report_type == "lost":
        matches = db.session.scalars(select(Match).filter_by(lost_item=target.id).order_by(Match.score.desc())).all()
        sorted_pairs = [(mat.found_item_obj, mat.score) for mat in matches]
    else:
        matches = db.session.scalars(select(Match).filter_by(found_item=target.id).order_by(Match.score.desc())).all()
        sorted_pairs = [(mat.lost_item_obj, mat.score) for mat in matches]

    return sorted_pairs


def all_sorted(
    filter_by_user: bool, by_creation_date: bool
) -> list[tuple[Report, Report, int, str]]:
    match_query = select(Match)
    if filter_by_user:
        match_query = match_query.filter(or_(Match.lost_item_obj.has(Report.author == current_user.id), Match.found_item_obj.has(Report.author == current_user.id)))

    if by_creation_date:
        match_query = match_query.order_by(Match.creation_date.desc(), Match.score.desc())
    else:
        match_query = match_query.order_by(Match.score.desc(), Match.creation_date.desc())

    matches = db.session.scalars(match_query).all()

    sorted_pairs = [(mat.lost_item, mat.found_item, mat.score, mat.creation_date.astimezone(org_timezone).strftime('%Y-%m-%d %H:%M')) for mat in matches]
    return sorted_pairs
