import json
import pymysql


def load_data():
    with open('E:\Flask\FlaskTpp\doc\data\cities.json','r',encoding='utf-8') as cities_json_file:
        cities_json_str = cities_json_file.read()#读
        cities_json = json.loads(cities_json_str)#加载内容  字典
    return cities_json


def insert_cities(json):
    cities_letter = cities_json.get('returnValue')

    keys =cities_letter.keys() #[A,B,C...]

    num =2

    for key in keys:

        cities = cities_letter.get(key) #城市
        num= num+1
        print(num)


        for city in cities:
            # print(city)

            c_id = city.get('id')
            c_parent_id = city.get('parentId')
            c_region_name = city.get('regionName')
            c_city_code = city.get('cityCode')
            c_pinyin = city.get('pinYin')


            db = pymysql.Connect(host='localhost', port=3306, user='root', password='chuang123456', database='FlaskTpp')

            cursor = db.cursor()
            cursor.execute("INSERT INTO city(letter_id, c_id, c_parent_id, c_region_name, c_city_code, c_pinyin) VALUES (%d,%d,%d,'%s',%d,'%s');" % (num,c_id,c_parent_id,c_region_name,c_city_code,c_pinyin))

            db.commit()

if __name__ == '__main__':
    cities_json = load_data()
    insert_cities(cities_json)