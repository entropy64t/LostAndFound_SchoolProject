from models import Grade, Category, Colour, Location, User, Report, Match
from sqlalchemy import delete, select, or_
from app import app, db
from flask import current_app
from flask_login import current_user

import threading
from datetime import datetime, timezone

from app import org_timezone
from models import get_location

def score_single(target: Report, item: Report) -> int:
    """Score `item` against `target` on a [0, 100] scale
 - `target` == `item` => 0
 - `target` and `item` have the same report type => 0
 - `target` and `item` have different item category => 0
 - `target` and `item` have different colours => 1 (TODO actual colour comparison)
 - `target` and `item` have same colour => 10
 - same `location` => 20
 - same `location.level` => 10
 - different locations => 0
 - share of words of shorter title having equivalents in longer title => 0 - 40
    
 - total: 0 - 100
    """
    if target == item: return 0
    if target.report_type == item.report_type: return 0
    if target.category != item.category: return 0
    
    colour_score = 10 if target.colour == item.colour else 1

    loc_score = 0
    target_loc = get_location(target.last_seen_location)
    item_loc = get_location(item.last_seen_location)
    if target_loc != None and item_loc != None:
        if target_loc == item_loc:
            loc_score = 20
        elif target_loc.building_level == item_loc.building_level:
            loc_score = 10

    ownership_score = 0
    if target.item_owner:
        if item.author:
            if target.item_owner == item.author:
                ownership_score = 30
    if item.item_owner:
        if target.author:
            if item.item_owner == target.author:
                ownership_score = 30

    title_score = 0
    if target.title and item.title:
        if len(target.title) <= len(item.title):
            a = target.title.lower()
            b = item.title.lower()
        else:
            a = item.title.lower()
            b = target.title.lower()
        a_words = a.split(' ')
        counter = 0
        for a_word in a_words:
            if a_word in b:
                counter += 1
        counter *= 40 # scale to [0, 40]
        total = len(a_words)
        title_score += counter // total

    total_score = colour_score + loc_score + ownership_score + title_score
    print("total: " + str(total_score))
    return total_score

def score_against(target: Report, items: list[Report]) -> dict[Report, int]:
    """Score `items` against `target`. For criteria look at `score_single`"""
    
    return {item: score_single(target, item) for item in items}

def sort_by_score(target: Report) -> list[tuple[Report, int]]:
    if target.report_type == "lost":
        matches = db.session.scalars(select(Match).filter_by(lost_item=target.id).order_by(Match.score.desc())).all()
        sorted_pairs = [(mat.found_item_obj, mat.score) for mat in matches]
    else:
        matches = db.session.scalars(select(Match).filter_by(found_item=target.id).order_by(Match.score.desc())).all()
        sorted_pairs = [(mat.lost_item_obj, mat.score) for mat in matches]
    
    
    return sorted_pairs

def all_sorted(filter_by_user, by_creation_date) -> list[tuple[Report, Report, int, str]]: # lost, found, score, created
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

def scoring_service(ctx, root: Report, report_list: list[Report], app):
    with ctx:
        scoring_result = score_against(root, report_list)
        db.session.execute(delete(Match).where(or_(Match.lost_item == root.id, Match.found_item == root.id)))
        db.session.commit()
        for pair in scoring_result:
            if scoring_result[pair] >= 10: # scoring threshold
                if root.report_type == "lost":
                    lost_item_id = root.id
                    found_item_id = pair.id
                else:
                    lost_item_id = pair.id
                    found_item_id = root.id

                mat = Match(lost_item=lost_item_id, found_item=found_item_id, score=scoring_result[pair], creation_date=datetime.now(timezone.utc))
                db.session.add(mat)
        db.session.commit()
        db.session.remove()

def update_scoring_of_report(root: Report):
    report_list = db.session.scalars(select(Report)).all()
    thread = threading.Thread(target=scoring_service, daemon=True, args=(app.app_context(), root, report_list, current_app._get_current_object()))
    thread.start()
