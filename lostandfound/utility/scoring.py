import threading
from datetime import datetime, timezone

from coloraide import Color
from flask import Flask, current_app
from flask_login import current_user
from rapidfuzz import fuzz
from sqlalchemy import delete, or_

from lostandfound import timezone as org_timezone
from lostandfound import db
from lostandfound.models import Colour, Match, Report, get_location, get_report

_MAX_DELTA_E_VALUE = 20


def _colour_similarity(a: Colour, b: Colour):
    if not a or not b:
        return 0
    c1 = Color(a.colour_value).convert("lab")
    c2 = Color(b.colour_value).convert("lab")

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
    # TODO make it 0-100 actually
    if target == item:
        return 0
    if target.report_type == item.report_type:
        return 0
    if target.category != item.category:
        return 0

    colour_score = _colour_similarity(target.colour, item.colour)

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
            fuzz.token_set_ratio(target.title, item.title) * 0.2
        )  # toke_set_ration returns [0, 100], so to make the title not have a very large impact scale it down by 5

    return colour_score + loc_score + ownership_score + title_score


def score_against(target: Report, items: list[Report]) -> dict[Report, int]:
    """Score `items` against `target`. For criteria look at `score_single`"""

    return {item: score_single(target, item) for item in items}


# TODO remove the type ignores


def scoring_service(root: Report, report_list: list[Report], app: Flask):
    with app.app_context():
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
    report_list = Report.query.all()
    thread = threading.Thread(
        target=scoring_service,
        daemon=True,
        args=(root, report_list, current_app._get_current_object()),  # type: ignore
    )
    thread.start()


def sort_by_score(target: Report) -> list[tuple[Report, int]]:
    if target.report_type == "lost":
        matches = Match.query.filter_by(lost_item=target.id).all()
        unsorted_pairs = {
            get_report(match.found_item): match.score for match in matches
        }
    else:
        matches = Match.query.filter_by(found_item=target.id).all()
        unsorted_pairs = {get_report(match.lost_item): match.score for match in matches}

    return sorted(unsorted_pairs.items(), key=lambda item: item[1], reverse=True)


def all_sorted(
    filter_by_user: bool, by_creation_date: bool
) -> list[tuple[Report, Report, int, str]]:
    matches = Match.query.all()
    if filter_by_user:
        for match in list(matches):
            if (
                get_report(match.lost_item).author != current_user.id
                and get_report(match.found_item).author != current_user.id
            ):
                matches.remove(match)

    unsorted_pairs = [
        (
            match.lost_item,
            match.found_item,
            match.score,
            match.creation_date.astimezone(org_timezone).strftime("%Y-%m-%d %H:%M"),
        )
        for match in matches
    ]

    if by_creation_date:
        sorted_pairs = sorted(unsorted_pairs, key=lambda item: item[2], reverse=True)
        return sorted(sorted_pairs, key=lambda item: item[3], reverse=True)

    sorted_pairs = sorted(unsorted_pairs, key=lambda item: item[3], reverse=True)
    return sorted(sorted_pairs, key=lambda item: item[2], reverse=True)
