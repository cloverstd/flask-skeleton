# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 15:36

from flask_restful import Resource, reqparse
from ..helpers import HackArgument


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser(argument_class=HackArgument, trim=True)
        super(BaseResource, self).__init__(*args, **kwargs)


class AuthResource(BaseResource):
    pass
