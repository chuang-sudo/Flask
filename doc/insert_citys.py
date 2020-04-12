import json
import pymysql


def load_data():
    with open('E:\Flask\FlaskTpp\doc\data\cities.json','r',encoding='utf-8') as cities_json_file:
        content = cities_json_file.read()#读
        cities_json = json.loads(content)#加载内容  字典
    return cities_json


def insert_cities(json):
    cities_letter = json.get('returnValue')

    keys =cities_letter.keys() #[A,B,C...]

    print(keys)
    num = 0



    for key in keys:

        cities = cities_letter.get(key) #城市
        num= num+1
        print(num)
        db = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', database='FlaskTpp')

        cursor = db.cursor()
        cursor.execute("INSERT INTO common_letter(letter) VALUES ('%s');" % (key))

        db.commit()


        for city in cities:
            # print(city)

            c_id = city.get('id')
            c_parent_id = city.get('parentId')
            c_region_name = city.get('regionName')
            c_city_code = city.get('cityCode')
            c_pinyin = city.get('pinYin')


            db = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', database='FlaskTpp')

            cursor = db.cursor()
            cursor.execute("INSERT INTO common_city(letter_id, c_id, c_parent_id, c_region_name, c_city_code, c_pinyin) VALUES (%d,%d,%d,'%s',%d,'%s');" % (num,c_id,c_parent_id,c_region_name,c_city_code,c_pinyin))

            db.commit()

if __name__ == '__main__':
    cities_json = load_data()
    insert_cities(cities_json)