from sqlalchemy import Enum as SQLAEnum
from app import db

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