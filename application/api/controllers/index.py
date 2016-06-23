# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:24

from flask import Blueprint
from ..helpers import Api
from ._base import BaseResource

bp = Blueprint(
    'index',
    __name__,
    url_prefix="",
)

api = Api(bp)


@api.resource('/hello')
class Hello(BaseResource):

    def get(self):
        return {'task': 'Say Hello'}
