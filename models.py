from sqlalchemy import Enum as SQLAEnum, select
from app import db
from flask import session
from typing import Optional
import numpy as np
from skimage.color import rgb2lab
from matplotlib import colors as mcolors

reportType = SQLAEnum('lost', 'found', name='reportType')

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    
    creation_date = db.Column(db.DateTime(timezone=True))
    author = db.Column(db.Integer)
    report_type = db.Column('type', reportType, nullable=False)
    
    category = db.Column(db.Integer)
    colour = db.Column(db.Integer)
    
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    image_urls = db.Column(db.String(255))
    
    last_seen = db.Column(db.DateTime(timezone=True))
    last_seen_location = db.Column(db.Integer)
    
    item_owner = db.Column(db.Integer)
    
    pickup_location = db.Column(db.Integer)

def get_report(report_id: int) -> Report:
    return Report.query.get(report_id)

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String())

def get_grade(grade_id: int) -> Grade:
    return Grade.query.get(grade_id)

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String())
    name_pl = db.Column(db.String())

    def localized_name(self) -> str:
        if session.get('lang') == 'pl':
            return self.name_pl
        else:
            return self.name

def get_category(category_id: int) -> Category:
    return Category.query.get(category_id)

class Colour(db.Model):
    __tablename__ = "colours"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String())
    display_name = db.Column(db.String())
    display_name_pl = db.Column(db.String())
    colour_value = db.Column(db.String())

    def localized_name(self) -> str:
        if session.get('lang') == 'pl':
            return self.display_name_pl
        else:
            return self.display_name

def get_colour(colour_id: int) -> Colour:
    return Colour.query.get(colour_id)

def _hex_to_rgb(hexstr: str) -> tuple[int, int, int]:
    s = hexstr.lstrip('#')
    if len(s) == 3:
        s = ''.join([c*2 for c in s])
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)

def distance(a: Colour, b: Colour) -> float:
    # Use skimage to convert sRGB to Lab and compute CIE76 Delta E
    ar, ag, ab = _hex_to_rgb(a.colour_value)
    br, bg, bb = _hex_to_rgb(b.colour_value)

    rgb1 = np.array([[[ar / 255.0, ag / 255.0, ab / 255.0]]], dtype=float)
    rgb2 = np.array([[[br / 255.0, bg / 255.0, bb / 255.0]]], dtype=float)
    lab1 = rgb2lab(rgb1)[0, 0]
    lab2 = rgb2lab(rgb2)[0, 0]

    return float(np.linalg.norm(lab1 - lab2))


def get_closest_colour(colour: Colour) -> tuple[float, Optional[Colour]]:
    colours = db.session.execute(select(Colour)).scalars().all()
    if len(colours) < 1:
        return (float("inf"), None)
    pairs = sorted((distance(colour, c), c) for c in colours)
    return pairs[0]


# XKCD colour lookup table (from matplotlib)
XKCD_COLORS = {k.replace('xkcd:', '').lower(): v for k, v in mcolors.XKCD_COLORS.items()}


def get_xkcd_hex(name: str) -> Optional[str]:
    if not name:
        return None
    return XKCD_COLORS.get(name.lower())


def get_name_from_hex(hexstr: str) -> Optional[str]:
    """Return the closest XKCD colour name for the given hex string.

    Returns None if input is invalid or table is empty.
    """
    if not hexstr:
        return None

    try:
        ar, ag, ab = _hex_to_rgb(hexstr)
    except Exception:
        return None

    rgb1 = np.array([[[ar / 255.0, ag / 255.0, ab / 255.0]]], dtype=float)
    lab1 = rgb2lab(rgb1)[0, 0]

    best_name = None
    best_dist = float('inf')

    for name, val in XKCD_COLORS.items():
        try:
            r, g, b = mcolors.to_rgb(val)
        except Exception:
            # skip malformed entry
            continue
        rgb2 = np.array([[[r, g, b]]], dtype=float)
        lab2 = rgb2lab(rgb2)[0, 0]
        dist = float(np.linalg.norm(lab1 - lab2))
        if dist < best_dist:
            best_dist = dist
            best_name = name

    return best_name

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)

    building_level = db.Column(db.Integer)
    name = db.Column(db.String())

    def location_string(self) -> str:
        if session.get('lang') == 'pl':
            level_str = "poziom"
        else:
            level_str = "level"
        return self.name + " (" + level_str + " " + str(self.building_level) + ")"

def get_location(location_id: int) -> Location:
    return Location.query.get(location_id)

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)

    lost_item = db.Column(db.Integer)
    found_item = db.Column(db.Integer)
    score = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime(timezone=True))
