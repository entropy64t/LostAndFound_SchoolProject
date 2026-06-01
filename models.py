from sqlalchemy import Enum as SQLAEnum
from app import db
from flask import session

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
    colour_value = db.Column(db.Integer)

    def localized_name(self) -> str:
        if session.get('lang') == 'pl':
            return self.display_name_pl
        else:
            return self.display_name

def get_colour(colour_id: int) -> Colour:
    return Colour.query.get(colour_id)

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
