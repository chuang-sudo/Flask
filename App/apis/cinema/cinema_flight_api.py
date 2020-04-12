import time

from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.apis_constant import HTTP_CREATE_OK, HTTP_OK
from App.apis.cinema.cinema_user_utils import login_require, require_permission
from App.models.cinema.cinema_address_model import CinemaAddress
from App.models.cinema.cinema_flight_model import Flight
from App.models.cinema.cinema_hall_model import Hall
from App.models.cinema.cinema_movie_model import CinemaMovie
from App.models.cinema.cinema_user_constant import PERMISSION_WRITE

parse = reqparse.RequestParser()
parse.add_argument('movie_id',required=True,help='请选择电影')
parse.add_argument('hall_id',required=True,help='请选择大厅')
parse.add_argument('time',required=True,help='请选择排挡时间')

flight_fields = {
    'id':fields.Integer,
    'f_movie_id':fields.Integer,
    'f_hall_id':fields.Integer,
    'f_time':fields.DateTime,
    'f_price':fields.Float
}

multi_flight_fields =  {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.List(fields.Nested(flight_fields))
}


class CinemaFlightsResource(Resource):
    @require_permission(PERMISSION_WRITE)
    def post(self):
        user_id = g.user.id
        args = parse.parse_args()
        f_movie_id = args.get('movie_id')
        f_hall_id = args.get('hall_id')
        f_time = args.get('time')

        cinema_movie = CinemaMovie.query.filter(CinemaMovie.c_cinema_id==user_id).filter(CinemaMovie.c_movie_id==f_movie_id).first()
        if not cinema_movie:
            abort(403,msg='该电影未购买')
        cinema_addresses = CinemaAddress.query.filter(CinemaAddress.c_user_id==user_id).all()
        cinema_addresses_id = []
        for cinema_address in cinema_addresses:
            cinema_addresses_id.append(cinema_address.id)

        hall = Hall.query.get(f_hall_id)
        print(hall.h_address_id)

        if not hall.h_address_id in cinema_addresses_id:
            abort(403,msg='影院不存在该大厅')


        flight = Flight()
        flight.f_movie_id = f_movie_id
        flight.f_hall_id = f_hall_id
        flight.f_time = f_time

        if not flight.save():
            abort(400,msg='档期创建失败')
        data = {
            'status':HTTP_CREATE_OK,
            'msg':'档期创建成功',
            'data':marshal(flight,flight_fields)
        }
        return data

    def get(self):
        pass