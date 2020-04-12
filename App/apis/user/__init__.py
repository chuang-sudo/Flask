from flask_restful import Api

from App.apis.user.movie_filter_api import UserFiltersResource, UserFilterResource
from App.apis.user.movie_order_api import OrdersResource, OrderResource
from App.apis.user.movie_order_pay_api import MovieOrderPayResource
from App.apis.user.movie_top_api import MovieTopResource
from App.apis.user.movie_user_api import MovieUsersResource

client_api = Api(prefix='/user')

client_api.add_resource(MovieUsersResource, '/movieusers/')

client_api.add_resource(OrdersResource, '/movieorders/')
client_api.add_resource(OrderResource, '/movieorders/<int:order_id>/')

client_api.add_resource(UserFiltersResource,'/moviefilter/')
client_api.add_resource(UserFilterResource,'/moviefilter/<int:flight_id>/')

client_api.add_resource(MovieOrderPayResource,'/movieorderpay/<int:order_id>/')

client_api.add_resource(MovieTopResource,'/movietop/')