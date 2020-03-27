from flask import request
from flask_restful import Resource, reqparse, fields, abort, marshal

from App.apis.admin.admin_user_utils import login_require
from App.apis.apis_constant import HTTP_CREATE_OK, HTTP_OK
from App.apis.common.movie_utils import filename_transfer
from App.models.common.movie_model import Movie
from App.settings import FILE_PATH_PREFIX, UPLOADS_DIR

parse = reqparse.RequestParser()
parse.add_argument('showname',required=True,help='must supply showname')
parse.add_argument('shownameen',required=True,help='must supply shownameen')
parse.add_argument('director',required=True,help='must supply director')
parse.add_argument('leadingRole',required=True,help='must supply leadingRole')
parse.add_argument('type',required=True,help='must supply type')
parse.add_argument('country',required=True,help='must supply country')
parse.add_argument('language',required=True,help='must supply language')
parse.add_argument('duration',required=True,help='must supply duration')
parse.add_argument('screen',required=True,help='must supply screen')
parse.add_argument('openday',required=True,help='must supply openday')
# parse.add_argument('backgroundpicture',required=True,help='must supply backgroundpicture')


movie_fields = {
    'showname':fields.String,
    'shownameen':fields.String,
    'director':fields.String,
    'leadingRole':fields.String,
    'type':fields.String,
    'country':fields.String,
    'language':fields.String,
    'duration':fields.String,
    'screen':fields.String,
    'openday':fields.DateTime,
    'backgroundpicture':fields.String
}

single_movie_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.Nested(movie_fields)
}

class MoviesResource(Resource):
    def get(self):
        return {'msg':'get ok'}

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