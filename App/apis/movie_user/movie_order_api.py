from flask import g
from flask_restful import Resource, reqparse, abort
from App.apis.movie_user.movie_user_utils import get_movie_user, login_require, require_permission
from App.ext import cache
from App.models.movie_user.model_constant import VIP_USER, COMMON_USER


class MovieOrdersResource(Resource):

    @login_require
    def post(self):
        user = g.user
        return {'msg':'post order ok'}


class MovieOrderResource(Resource):
    @require_permission(VIP_USER)
    def put(self,order_id):

        return {'msg':'change success'}

