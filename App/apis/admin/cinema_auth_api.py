from flask_restful import Resource, marshal, fields, reqparse, abort

from App.apis.admin.admin_user_utils import login_require
from App.apis.apis_constant import HTTP_OK
from App.apis.cinema.cinema_user_api import cinema_user_fields
from App.models.cinema.cinema_user_model import CinemaUser

multi_cinema_user_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.List(fields.Nested(cinema_user_fields))
}

class CinemaUsersAuthResource(Resource):
    @login_require
    def get(self):
        cinema_users = CinemaUser.query.all()
        data = {
            'status':HTTP_OK,
            'msg':'get cinema users ok',
            'data':cinema_users
        }
        return marshal(data,multi_cinema_user_fields)


parse = reqparse.RequestParser()
parse.add_argument('is_verify',type=bool,required=True,help='请提供操作')

class CinemaUserAuthResource(Resource):
    @login_require
    def get(self,id):
        cinema_user = CinemaUser.query.get(id)
        data = {
            'status':HTTP_OK,
            'msg':'get cinema users ok',
            'data':marshal(cinema_user,cinema_user_fields)
        }
        return data

    @login_require
    def patch(self,id):
        args = parse.parse_args()
        is_verify = args.get('is_verify')

        cinema_user = CinemaUser.query.get(id)
        if not cinema_user:
            abort(400,msg='cinema user donot exist')
        cinema_user.is_verify = is_verify

        if not cinema_user.save():
            abort(400,msg='cannot patch cinema user successfully')
        data = {
            'status':HTTP_OK,
            'msg':'patch cinema user successfully',
            'data':marshal(cinema_user,cinema_user_fields)
        }
        return data