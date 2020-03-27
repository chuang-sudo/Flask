from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.apis_constant import HTTP_CREATE_OK
from App.apis.cinema_admin.cinema_address_utils import require_permission
from App.models.cinema_admin.cinema_address_model import CinemaAddress
from App.models.cinema_admin.cinema_user_constant import PERMISSION_WRITE

parse = reqparse.RequestParser()
parse.add_argument('name',required=True,help='请提供影院名字')
parse.add_argument('phone',required=True,help='请提供联系方式')
parse.add_argument('city',required=True,help='请提供城市')
parse.add_argument('district',required=True,help='请提供所在区')
parse.add_argument('address',required=True,help='请提供详细地址')


cinema_fields = {
    'c_user_id':fields.Integer,
    'name':fields.String,
    'phone':fields.String,
    'city':fields.String,
    'district':fields.String,
    'address':fields.String,
    'score':fields.Float,
    'servicecharge':fields.Float,
    'astrict':fields.Float,
    'hallnum':fields.Integer,
    'flag':fields.Boolean,
    'is_delete':fields.Boolean
}


class CinemaAddressesResource(Resource):
    def get(self):
        pass

    @require_permission(PERMISSION_WRITE)
    def post(self):
        args =parse.parse_args()

        name = args.get('name')
        phone = args.get('phone')
        district = args.get('district')
        city = args.get('city')
        address = args.get('address')

        cinema_address = CinemaAddress()
        cinema_address.c_user_id = g.user.id
        cinema_address.name = name
        cinema_address.city = city
        cinema_address.phone = phone
        cinema_address.district = district
        cinema_address.address =address

        if not cinema_address.save():
            abort(400,msg='cannot save cinema successfully')

        data = {
            'status':HTTP_CREATE_OK,
            'msg':'create cinema ok',
            'data':marshal(cinema_address,cinema_fields)
        }
        return data
class CinemaAddressResource(Resource):
    pass