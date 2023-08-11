"""
开发的时候，可能连接的是开发环境的数据库，在测试的时候，可能连接的是测试服务器的数据库，在上线后，则需要更换成线上服务器的数据库。
为了满足不同配置，我们在config.py中根据环境创建不同的类。
开发 -- DevelopmentConfig
测试 -- TestingConfig
线上环境 -- ProductionConfig
"""
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
# 理论上写的越长越安全, 越长解密的时候越慢
# SECRET_KEY = "asdfdgrahlsdjhfaldjkbguq"

# docker run --name quest3305 -p 3305:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_USER=lexiyin -e
# MYSQL_PASSWORD=pwd123 -e MYSQL_DATABASE=questDB -d mysql

HOSTNAME = '127.0.0.1'
PORT     = 3305
DATABASE = 'questDB'
USERNAME = 'lexiyin'
PASSWORD = 'pwd123'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# mail configuration
MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

# Cache configuration
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379
# CACHE_DEFAULT_TIMEOUT = xxx  # 默认是300s