# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:02

from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/application"
    CELERY_BROKER_URL = 'redis://11.11.11.3:6379/0'

