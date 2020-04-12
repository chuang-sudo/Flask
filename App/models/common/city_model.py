
from App.ext import db
from App.models import BaseModel


class Letter(BaseModel):
    __tablename__ = 'common_letter'
    letter = db.Column(db.String(1),unique=True)

class City(BaseModel):
    __tablename__ = 'common_city'
    letter_id = db.Column(db.Integer,db.ForeignKey(Letter.id))
    c_id = db.Column(db.Integer,default=0)
    c_parent_id = db.Column(db.Integer,default=0)
    c_region_name = db.Column(db.String(16))
    c_city_code = db.Column(db.Integer,default=0)
    c_pinyin = db.Column(db.String(64))