import datetime

from flask import g
from flask_restful import Resource, reqparse, abort, marshal, fields
from sqlalchemy import or_

from App.apis.apis_constant import HTTP_CREATE_OK, HTTP_OK
from App.apis.user.movie_user_utils import  login_require, require_permission
from App.ext import cache
from App.models.cinema.cinema_flight_model import Flight
from App.models.cinema.cinema_hall_model import Hall
from App.models.user.model_constant import VIP_USER, COMMON_USER
from App.models.user.movie_order_model import MovieOrder, ORDER_STATUS_PAYED_NOT_GET, ORDER_STATUS_GET, \
    ORDER_STATUS_NOT_PAY

parse = reqparse.RequestParser()
parse.add_argument('o_flight_id',required=True,type=int,help='请选择电影档期')
parse.add_argument('o_seat',required=True,help='请选择座位')

order_fields = {
    'id':fields.Integer,
    'o_user_id':fields.Integer,
    'o_flight_id':fields.Integer,
    'o_seat':fields.String,
    'o_price':fields.Integer,
    'o_time':fields.DateTime
}

multi_order_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.List(fields.Nested(order_fields))
}

class OrdersResource(Resource):
    @login_require
    def get(self):
        user = g.user
        orders = MovieOrder.query.filter(MovieOrder.o_user_id==user.id)
        data = {
            'status':HTTP_OK,
            'msg':'查询订单成功',
            'data':orders
        }
        return marshal(data,multi_order_fields)
    @login_require
    def post(self):
        user = g.user
        args = parse.parse_args()
        o_flight_id = args.get('o_flight_id')
        o_seat = args.get('o_seat')
        flight  = Flight.query.get(o_flight_id)
        print(flight)
        hall = Hall.query.get(flight.f_hall_id)
        seats = hall.h_seats.split('#')

        sold_seats = []
        flight_orders = MovieOrder.query.filter(MovieOrder.o_flight_id==o_flight_id)
        orders_payed = flight_orders.filter(or_(MovieOrder.o_status==ORDER_STATUS_PAYED_NOT_GET,MovieOrder.o_status==ORDER_STATUS_GET))
        orders_not_pay = flight_orders.filter(MovieOrder.o_status==ORDER_STATUS_NOT_PAY).filter(MovieOrder.o_time>datetime.datetime.now())
        for order_payed in orders_payed:
            sold_seats += order_payed.o_seat.split('#')
        for order_not_pay in orders_not_pay:
            sold_seats += order_not_pay.o_seat.split('#')

        want_buy = o_seat.split('#')
        for item in want_buy:
            if item not in seats:
                abort(400,msg='锁座失败')
            if item in sold_seats:
                abort(400,msg='锁座失败')
 
        order = MovieOrder()
        order.o_price = flight.f_price * len(want_buy)
        order.o_flight_id = o_flight_id
        order.o_user_id = user.id
        order.o_seat =o_seat

        order.o_time = datetime.datetime.now() + datetime.timedelta(minutes=15)

        if not order.save():
            abort(400,msg='下单失败')
        data = {
            'status':HTTP_CREATE_OK,
            'msg':'下单成功',
            'data':marshal(order,order_fields)
        }
        return data


class OrderResource(Resource):
    @require_permission(VIP_USER)
    def put(self,order_id):

        return {'msg':'change success'}

