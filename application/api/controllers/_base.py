# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 15:36

from flask_restful import Resource, reqparse
from ..helpers import HackArgument

from application.utils.helper import SuccessOutput, ErrorOutput


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser(argument_class=HackArgument, trim=True)
        super(BaseResource, self).__init__(*args, **kwargs)

    def success(self, data=None, message=None, code=0):
        return SuccessOutput(data, code, message)

    def error(self, code, message=None, data=None):
        return ErrorOutput(code=code, message=message, data=data)


class AuthResource(BaseResource):
    pass
