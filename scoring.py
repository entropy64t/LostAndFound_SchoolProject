from models import Report, get_location

def score_single(target: Report, item: Report) -> float:
    """Score `item` against `target` on a [0, 1] scale
 - `target` == `item` => 0
 - `target` and `item` have the same report type => 0
 - `target` and `item` have different item category => 0
 - `target` and `item` have different colours => 0.01 (TODO actual colour comparison)
 - `target` and `item` have same colour => 0.1
 - same `location` => 0.2
 - same `location.level` => 0.1
 - different locations => 0
    
    """
    if target == item: return 0
    if target.report_type == item.report_type: return 0
    if target.category != item.category: return 0
    
    colour_score = 0.1 if target.colour == item.colour else 0.01
    loc_score = 0
    target_loc = get_location(target.last_seen_location)
    item_loc = get_location(item.last_seen_location)
    loc_score = 0.1 if target_loc.building_level == item_loc.building_level else 0
    loc_score = 0.2 if target_loc == item_loc else 0
    
    return colour_score + loc_score

def score_against(target: Report, items: list[Report]) -> dict[Report, float]:
    """Score `items` against `target`. For criteria look at `score_single`"""
    
    return {item: score_single(target, item) for item in items}

def sort_by_score(target: Report, items: list[Report]) -> list[tuple[Report, float]]:
    scores = score_against(target, items)
    
    sorted_pairs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    return [pair for pair in sorted_pairs if pair[1] != 0] # delete ones that scored 0