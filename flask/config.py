import os

MAIL_USERNAME = "ENTER YOUR EMAIL HERE"
MAIL_PASSWORD = "ENTER PW HERE"

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

SECRET_KEY = 'ssuxAAY7iT'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

JWT_SECRET_KEY = 'laendQEdwi23'

UPLOAD_FOLDER = basedir + r'\posts'
MAX_CONTENT_PATH = 5000000

CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
# CELERY_REDIS_USERNAME = 'default'
# CELERY_REDIS_PASSWORD = 'redispw'
CELERY_TIMEZONE = "Asia/Kolkata"

MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = ('SandiBot', MAIL_USERNAME)
MAIL_USE_TLS = False
MAIL_USE_SSL = True

CACHE_TYPE = 'RedisCache'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_REDIS_URL = 'redis://localhost:6379/0'
CACHE_DEFAULT_TIMEOUT = 500