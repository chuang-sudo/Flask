from App.ext import db
from App.models import BaseModel
from App.models.cinema.cinema_hall_model import Hall
from App.models.common.movie_model import Movie


class Flight(BaseModel):
    __tablename__ = 'cinema_flight'
    f_movie_id = db.Column(db.Integer,db.ForeignKey(Movie.id))
    f_hall_id = db.Column(db.Integer,db.ForeignKey(Hall.id))
    f_time = db.Column(db.DateTime)
    f_price = db.Column(db.Float,default=40.0)

    movieorder = db.relationship('MovieOrder',backref='Flight',lazy=True)