import datetime

from flask_restful import Resource, reqparse, marshal
from sqlalchemy import or_

from App.apis.apis_constant import HTTP_OK
from App.apis.cinema.cinema_address_api import multi_cinema_fields
from App.apis.cinema.cinema_flight_api import multi_flight_fields
from App.apis.cinema.cinema_hall_api import hall_fields
from App.apis.user.movie_user_utils import login_require
from App.models.cinema.cinema_address_model import CinemaAddress
from App.models.cinema.cinema_flight_model import Flight
from App.models.cinema.cinema_hall_model import Hall
from App.models.user.movie_order_model import MovieOrder, ORDER_STATUS_PAYED_NOT_GET, ORDER_STATUS_NOT_PAY, \
    ORDER_STATUS_GET

parse = reqparse.RequestParser()
parse.add_argument('cinema_user_id',type=int,required=True)
parse.add_argument('district',type=str,required=True)
parse.add_argument('movie_id')

ALL = 0

class UserFiltersResource(Resource):
    def get(self):
        args = parse.parse_args()
        cinema_user_id = args.get('cinema_user_id')
        district = args.get('district')
        movie_id = args.get('movie_id')
        #两个参数筛选影院
        cinema_addresses = CinemaAddress.query.all()
        if district == str(ALL):
            pass
        else:
            cinema_addresses = CinemaAddress.query.filter_by(district=district)
        if cinema_user_id == ALL:
            pass
        else:
            cinema_addresses = cinema_addresses.filter_by(c_user_id=cinema_user_id)
            print('ok')
        #三个参数筛选排挡
        if movie_id:
            all_halls = []
            for cinema_address in cinema_addresses:
                halls = Hall.query.filter_by(h_address_id=cinema_address.id).all()
                all_halls += halls
            data ={}

            flights = []
            for hall in all_halls:
                flights += Flight.query.filter(Flight.f_hall_id==hall.id).filter(Flight.f_movie_id==movie_id)
                data = {
                    'status':HTTP_OK,
                    'msg':'筛选排档成功',
                    'data':flights
                }
            return marshal(data,multi_flight_fields)

        else:
            data = {
                'status':HTTP_OK,
                'msg':'筛选影院',
                'data':cinema_addresses
            }
            return marshal(data,multi_cinema_fields)


class UserFilterResource(Resource):
    @login_require
    def get(self, flight_id):
        flight = Flight.query.get(flight_id)
        hall = Hall.query.get(flight.f_hall_id)

        flight_orders = MovieOrder.query.filter(MovieOrder.o_flight_id == flight_id)

        lock_seats = []
        orders_payed = flight_orders.filter(
            or_(MovieOrder.o_status == ORDER_STATUS_PAYED_NOT_GET, MovieOrder.o_status == ORDER_STATUS_GET))
        orders_not_pay = flight_orders.filter(MovieOrder.o_status == ORDER_STATUS_NOT_PAY).filter(
            MovieOrder.o_time > datetime.datetime.now())
        for order_payed in orders_payed:
            lock_seats += order_payed.o_seat.split('#')
        for order_not_pay in orders_not_pay:
            lock_seats += order_not_pay.o_seat.split('#')


        all_seats = hall.h_seats.split('#')
        can_buy = list(set(all_seats) - set(lock_seats))

        data = {
            'status':HTTP_OK,
            'msg':'点击排挡进入大厅',
            'data':marshal(hall,hall_fields),
            'can_buy':can_buy
        }
        return data