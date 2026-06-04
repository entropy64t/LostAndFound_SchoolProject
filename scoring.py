from models import Report, get_location, Match
from sqlalchemy import delete, or_
from app import app, db
from flask import current_app

import threading

def score_single(target: Report, item: Report) -> float:
    """Score `item` against `target` on a [0, 100] scale
 - `target` == `item` => 0
 - `target` and `item` have the same report type => 0
 - `target` and `item` have different item category => 0
 - `target` and `item` have different colours => 1 (TODO actual colour comparison)
 - `target` and `item` have same colour => 10
 - same `location` => 20
 - same `location.level` => 10
 - different locations => 0
    
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

    return colour_score + loc_score + ownership_score

def score_against(target: Report, items: list[Report]) -> dict[Report, float]:
    """Score `items` against `target`. For criteria look at `score_single`"""
    
    return {item: score_single(target, item) for item in items}

def sort_by_score(target: Report, items: list[Report]) -> list[tuple[Report, float]]:
    scores = score_against(target, items)
    
    sorted_pairs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    return [pair for pair in sorted_pairs if pair[1] != 0] # delete ones that scored 0

def scoring_service(root: Report, report_list: list[Report], app):
    with app.app_context():
        scoring_result = score_against(root, report_list)
        db.session.execute(delete(Match).where(or_(Match.lost_item == root.id, Match.found_item == root.id)))
        db.session.commit()
        for pair in scoring_result:
            if scoring_result[pair] > 0:
                if root.report_type == "lost":
                    lost_item_id = root.id
                    found_item_id = pair.id
                else:
                    lost_item_id = pair.id
                    found_item_id = root.id

                mat = Match(lost_item=lost_item_id, found_item=found_item_id, score=scoring_result[pair])
                db.session.add(mat)
        db.session.commit()
        db.session.remove()

def update_scoring_of_report(root: Report):
    report_list = Report.query.all()
    thread = threading.Thread(target=scoring_service, daemon=True, args=(root, report_list, current_app._get_current_object()))
    thread.start()
