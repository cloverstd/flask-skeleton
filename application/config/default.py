# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 10:59

import os
import datetime as dt

class Config(object):

    DEBUG = False

    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@host/database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_NAME = "flask-skeleton"
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SECRET_KEY = "secret key"

    JWT_AUTH_URL_RULE = '/user/auth'
    JWT_EXPIRATION_DELTA = dt.timedelta(seconds=3600 * 24)