from App.ext import db
from App.models import BaseModel
from App.models.cinema.cinema_flight_model import Flight
from App.models.user.movie_user_model import MovieUser

ORDER_STATUS_NOT_PAY = 0
ORDER_STATUS_PAYED_NOT_GET = 1
ORDER_STATUS_GET = 2
ORDER_STATUS_TIMEOUT = 3


class MovieOrder(BaseModel):
    __tablename__ = 'movie_order'
    o_user_id = db.Column(db.Integer, db.ForeignKey(MovieUser.id))
    o_flight_id = db.Column(db.Integer,db.ForeignKey(Flight.id))
    o_status = db.Column(db.Integer,default=ORDER_STATUS_NOT_PAY)
    o_time = db.Column(db.DateTime)
    o_seat = db.Column(db.String(128))
    o_price = db.Column(db.Float)