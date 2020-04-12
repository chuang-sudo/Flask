
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_uri(dbinfo):
    engine = dbinfo.get('ENGINE') or 'sqlite'
    driver = dbinfo.get('DRIVER') or 'sqlie'
    user = dbinfo.get('USER') or ''
    password = dbinfo.get('PASSWORD') or ''
    host = dbinfo.get('HOST') or ''
    port = dbinfo.get('PORT') or ''
    name = dbinfo.get('NAME') or ''
    return '{}+{}://{}:{}@{}:{}/{}'.format(engine,driver,user,password,host,port,name)


class Config:

    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'chuang'


class DevelopCofig(Config):

    DEBUG = True

    dbinfo = {
        'ENGINE':'mysql',
        'DRIVER':'mysqlconnector',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'localhost',
        'PORT':'3306',
        'NAME':'FlaskTpp'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

    """邮箱配置
    """
    MAIL_USERNAME = '2722466435@qq.com'
    MAIL_PASSWORD = 'lzythkazpfgeddhg'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class TestingConfig(Config):

    DEBUG = True

    dbinfo = {
        'ENGINE':'mysql',
        'DRIVER':'mysqlconnector',
        'USER':'root',
        'PASSWORD':'chuang123456',
        'HOST':'localhost',
        'PORT':'3306',
        'NAME':'FlaskTpp'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    DEBUG = True

    dbinfo = {
        'ENGINE':'mysql',
        'DRIVER':'mysqlconnector',
        'USER':'root',
        'PASSWORD':'chuang123456',
        'HOST':'localhost',
        'PORT':'3306',
        'NAME':'FlaskTpp'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagineConfig(Config):

    DEBUG = True

    dbinfo = {
        'ENGINE':'mysql',
        'DRIVER':'mysqlconnector',
        'USER':'root',
        'PASSWORD':'chuang123456',
        'HOST':'localhost',
        'PORT':'3306',
        'NAME':'FlaskTpp'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    'develop':DevelopCofig,
    'testing':TestingConfig,
    'stagine':StagineConfig,
    'product':ProductConfig,
    'default':DevelopCofig
}

ADMINS = ['chuang','root']

UPLOADS_DIR =os.path.join(BASE_DIR,'App/static/uploads/icons')

FILE_PATH_PREFIX = r'/static/uploads/icons'

#Alipay
ALIPAY_APPID = '2016101800714848'
ALIPAY_PRIVATE_KEY = open(os.path.join(BASE_DIR, 'alipay_config/rsa_private_key.pem'), 'r').read()
ALIPAY_PUBLIC_KEY = open(os.path.join(BASE_DIR, 'alipay_config/rsa_public_key.pem'), 'r').read()