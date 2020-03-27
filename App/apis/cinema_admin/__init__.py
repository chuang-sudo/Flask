from flask_restful import Api

from App.apis.cinema_admin.cinema_address_api import CinemaAddressesResource, CinemaAddressResource
from App.apis.cinema_admin.cinema_user_api import CinemaUsersResource

movie_client_api = Api(prefix='/cinema')

movie_client_api.add_resource(CinemaUsersResource, '/users/')
movie_client_api.add_resource(CinemaAddressesResource, '/addresses/')
movie_client_api.add_resource(CinemaAddressResource, '/addresses/<int:id>/')