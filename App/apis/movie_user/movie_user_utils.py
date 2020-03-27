from flask import request, g
from flask_restful import reqparse, abort

from App.ext import cache
from App.models.movie_user.movie_user_model import MovieUser
from App.utils import MOVIE_USER


def get_movie_user(user_ident):
    if not user_ident:
        return None
    #identify by id
    user = MovieUser.query.get(user_ident)
    if user:
        return user
    #identify by phone
    user = MovieUser.query.filter(MovieUser.phone == user_ident).first()
    if user:
        return user
    #identify by username
    user = MovieUser.query.filter(MovieUser.username == user_ident).first()
    if user:
        return user
    return None


parse = reqparse.RequestParser()
parse.add_argument('token')

def _verify():
    parameters = parse.parse_args()
    token = parameters.get('token')

    if not token:
        abort(401, msg='not login')

    if not token.startswith(MOVIE_USER):
        abort(403,msg='cannot access')

    user_id = cache.get(token)
    user = get_movie_user(user_id)

    if not user:
        abort(401, msg='user is not available')
    g.user = user
    g.auth = token




def login_require(fun):
    def wrapper(*args,**kwargs):
        _verify()
        return fun(*args,**kwargs)
    return wrapper


def require_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(*args,**kwargs):
            _verify()
            if not g.user.check_permission(permission):
                abort(403,msg='user can not access')

            return fun(*args,**kwargs)
        return wrapper
    return require_permission_wrapper