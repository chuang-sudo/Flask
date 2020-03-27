from flask_restful import Resource, fields, marshal

from App.apis.apis_constant import HTTP_OK
from App.models.common.city_model import City, Letter

city_fields = {
    'id':fields.Integer(attribute='c_id'),
    'parentId':fields.Integer(attribute='c_parent_id'),
    'regionName':fields.String(attribute='c_region_name'),
    'cityCode':fields.String(attribute='c_city_code'),
    'pinYin':fields.String(attribute='C-pinyin')

}



class CitiesResource(Resource):

    def get(self):
        letters = Letter.query.all()

        letters_cities_fileds = {}#fields模板
        json = {}
        for letter in letters:
            letters_cities_fileds[letter.letter] = fields.List(fields.Nested(city_fields))
            letter_cities = City.query.filter(City.letter_id==letter.id)#letter 级联 城市列表
            json[letter.letter] = letter_cities
        data = {
            'msg':'ok',
            'status':HTTP_OK,
            'data':marshal(json,letters_cities_fileds)
        }
        return data