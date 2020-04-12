import uuid

from flask_restful import fields, reqparse

from App.settings import UPLOADS_DIR, FILE_PATH_PREFIX


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

multi_movies_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.List(fields.Nested(movie_fields))
}




def filename_transfer(filename):
    ext_name = filename.rsplit(".")[1]
    new_filename = uuid.uuid4().hex + '.'+ext_name
    save_path = UPLOADS_DIR+'/'+new_filename
    upload_path = FILE_PATH_PREFIX+'/'+new_filename
    return save_path,upload_path

