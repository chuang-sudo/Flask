from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.apis_constant import HTTP_CREATE_OK, HTTP_OK
from App.apis.cinema.cinema_user_utils import require_permission, login_require
from App.models.cinema.cinema_address_model import CinemaAddress
from App.models.cinema.cinema_hall_model import Hall
from App.models.cinema.cinema_user_constant import PERMISSION_WRITE
from App.models.cinema.cinema_user_model import CinemaUser

parse = reqparse.RequestParser()
parse.add_argument('h_num',required=True,help='请提供放映厅编号')
parse.add_argument('h_seats',required=True,help='请提供座位数')
parse.add_argument('h_address_id',required=True,type=int,help='请提供电影院地址')

hall_fields = {
    'h_address_id':fields.Integer,
    'h_num':fields.Integer,
    'h_seats':fields.String
}

multi_hall_fields= {
    'halls':fields.List(fields.Nested(hall_fields))
}

class CinemaHallsResource(Resource):
    @require_permission(PERMISSION_WRITE)
    def post(self):
        user_id = g.user.id
        args = parse.parse_args()
        h_num = args.get('h_num')
        h_seats = args.get('h_seats')
        h_address_id = args.get('h_address_id')
        cinema_address = CinemaAddress.query.filter(CinemaAddress.c_user_id==user_id).filter(CinemaAddress.id==h_address_id).first()
        if not cinema_address:
            abort(400,msg='该影院不存在')
        hall = Hall()
        hall.h_num = h_num
        hall.h_address_id = h_address_id
        hall.h_seats = h_seats
        if not hall.save():
            abort(400,msg='放映厅创建失败')
        cinema_address.hallnum += 1
        if not cinema_address.save():
            abort(400,msg='同步影院信息失败')
        data = {
            'status':HTTP_CREATE_OK,
            'msg':'放映厅创建成功',
            'data':marshal(hall,hall_fields)
        }
        return data

    def get(self):
        pass