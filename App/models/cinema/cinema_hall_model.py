from App.ext import db
from App.models import BaseModel
from App.models.cinema.cinema_address_model import CinemaAddress


class Hall(BaseModel):
    __tablename__ = 'cinema_hall'
    h_address_id = db.Column(db.Integer,db.ForeignKey(CinemaAddress.id))
    h_num = db.Column(db.Integer,default=1)
    h_seats = db.Column(db.String(128))