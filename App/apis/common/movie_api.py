from flask import request
from flask_restful import Resource, abort, marshal

from App.apis.admin.admin_user_utils import login_require
from App.apis.apis_constant import HTTP_CREATE_OK, HTTP_OK
from App.apis.common.movie_utils import filename_transfer, parse, single_movie_fields, multi_movies_fields
from App.models.common.movie_model import Movie


class MoviesResource(Resource):
    def get(self):
        movies = Movie.query.all()
        data = {
            'status':HTTP_OK,
            'msg':'获取所有电影成功',
            'data':movies
        }
        return marshal(data,multi_movies_fields)

    @login_require #admin后端账户登录
    def post(self):

        args = parse.parse_args()
        showname = args.get('showname')
        shownameen = args.get('shownameen')
        director = args.get('director')
        leadingRole = args.get('leadingRole')
        type = args.get('type')
        country = args.get('country')
        duration = args.get('duration')
        screen = args.get('screen')
        openday = args.get('openday')
        backgroundpicture = request.files.get('backgroundpicture')
        print(backgroundpicture)


        movie = Movie()
        movie.showname = showname
        movie.shownameen = shownameen
        movie.director = director
        movie.leadingRole = leadingRole
        movie.type = type
        movie.country =country
        movie.duration = duration
        movie.screen =screen
        movie.openday = openday

        file_info = filename_transfer(backgroundpicture.filename)
        filepath ,filepath_relative= file_info
        backgroundpicture.save(filepath)
        movie.backgroundpicture = filepath_relative


        if not movie.save():
            abort(400,msg='cannot create successfully')

        data = {
            'status':HTTP_CREATE_OK,
            'msg':'create movie successfully',
            'data':movie
        }

        return marshal(data,single_movie_fields)

class MovieResource(Resource):
    def get(self,id):
        movie =  Movie.query.get(id)
        if not movie:
            abort(400,msg='movie doesnot exist')
        data = {
            'msg':'ok',
            'status':HTTP_OK,
            'data':movie
        }
        return marshal(data,single_movie_fields)

    @login_require
    def patch(self,id):
        pass

    @login_require
    def put(self,id):
        pass

    @login_require
    def delete(self,id):
        pass