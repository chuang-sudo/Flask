from flask_restful import Api

from App.apis.admin.admin_user_api import AdminUsersResource
from App.apis.admin.cinema_auth_api import CinemaUsersAuthResource, CinemaUserAuthResource
from App.apis.admin.cinema_permission_api import CinemaUserPermissionResource

admin_api = Api(prefix='/admin')

admin_api.add_resource(AdminUsersResource,'/users/')
admin_api.add_resource(CinemaUsersAuthResource,'/cinemausers/')
admin_api.add_resource(CinemaUserAuthResource,'/cinemausers/<int:id>/')
admin_api.add_resource(CinemaUserPermissionResource,'/cinemausersper/<int:id>/')