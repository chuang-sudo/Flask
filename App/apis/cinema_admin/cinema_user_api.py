from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.apis.apis_constant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from App.apis.cinema_admin.cinema_user_utils import get_cinema_user
from App.ext import cache
from App.models.cinema_admin.cinema_user_model import CinemaUser
from App.utils import  generate_cinema_user_token

cinema_user_fields = {
    'id':fields.Integer,
    'username':fields.String,
    'password':fields.String(attribute='_password'),
    'phone':fields.String,
    'is_delete':fields.Boolean,
    'is_verify':fields.Boolean
}

single_cinema_user_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.Nested(cinema_user_fields)
}

parse_base = reqparse.RequestParser()
parse_base.add_argument('action', type=str, required=True, help='请输入请求参数')
parse_base.add_argument('password', type=str, required=True, help='请输入密码')

parse_register = parse_base.copy()
parse_register.add_argument('phone', type=str, required=True, help='请输入手机号码')
parse_register.add_argument('username', type=str, required=True, help='请输入用户名')

parse_login = parse_base.copy()
parse_login.add_argument('phone', type=str)
parse_login.add_argument('username', type=str)

class CinemaUsersResource(Resource):


    def post(self):
        args = parse_base.parse_args()
        password = args.get('password')
        action = args.get('action').lower()

        if action == USER_ACTION_REGISTER:
            args_register = parse_register.parse_args()
            username = args_register.get('username')
            phone = args_register.get('phone')

            cinema_user = CinemaUser()
            cinema_user.username = username
            cinema_user.password = password
            cinema_user.phone = phone

            if not cinema_user.save():
                abort(400,msg='create fail')
            data = {
                'status':HTTP_CREATE_OK,
                'msg':'用户创建成功',
                'data':cinema_user
            }
            return marshal(data, single_cinema_user_fields)

        elif action == USER_ACTION_LOGIN:
            args_login = parse_login.parse_args()
            username = args_login.get('username')
            phone = args_login.get('phone')

            user = get_cinema_user(username) or get_cinema_user(phone)
            if not user:
                abort(400,msg='用户不存在')
            if not user.check_password(password):
                abort(401,msg='用户名或密码错误')
            if user.is_delete:
                abort(401,msg='用户不存在')

            token = generate_cinema_user_token()
            cache.set(token,user.id,timeout=60*60*24*7)
            data = {
                'status':HTTP_OK,
                'msg':'login success',
                'token':token
            }
            return data
        else:
            abort(400,msg='请输入正确的参数')