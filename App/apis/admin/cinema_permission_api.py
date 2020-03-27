from flask_restful import Resource, marshal, abort, reqparse

from App.apis.admin.admin_user_utils import login_require
from App.apis.admin.cinema_auth_api import multi_cinema_user_fields
from App.apis.apis_constant import HTTP_OK, HTTP_CREATE_OK
from App.apis.cinema_admin.cinema_user_api import cinema_user_fields
from App.models.cinema_admin.cinema_user_model import CinemaUser, Permission, CinemaUserPermission

parse = reqparse.RequestParser()
parse.add_argument('permission_name',type=str,required=True,help='请输入权限')



# class CinemaUsersPermissonResource(Resource):
#     @login_require
#     def get(self):
#         cinema_users = CinemaUser.query.all()
#         data = {
#             'status':HTTP_OK,
#             'msg':'get cinema users ok',
#             'data':cinema_users,
#         }
#         return marshal(data,multi_cinema_user_fields)


class CinemaUserPermissionResource(Resource):
    @login_require
    def post(self,id):
        cinema_user = CinemaUser.query.get(id)
        if not cinema_user:
            abort(400,msg='cinema user donot exist')

        args = parse.parse_args()

        permission_name =args.get('permission_name')
        permission = Permission.query.filter(Permission.p_name==permission_name).first()

        have_user_permissions = CinemaUserPermission.query.filter_by(c_user_id=id)
        for have_user_permission in have_user_permissions:
            if Permission.query.get(have_user_permission.c_permission_id).p_name == permission_name:
                abort(400,msg='已拥有该权限')

        cinema_user_permission = CinemaUserPermission()
        cinema_user_permission.c_user_id = id
        cinema_user_permission.c_permission_id = permission.id
        if not cinema_user_permission.save():
            abort(400,msg='影院用户权限表保存失败')

        user_permissions = cinema_user_permission.query.filter_by(c_user_id=id)
        p_name_list =[]
        for user_permission in user_permissions:
            p_name = Permission.query.get(user_permission.c_permission_id).p_name
            p_name_list.append(p_name)
        data = {
            'status':HTTP_CREATE_OK,
            'msg':'创建影院权限成功',
            'data':marshal(cinema_user,cinema_user_fields),
            'permissions_name_list':p_name_list
        }

        return data