# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 17:10

from ._base import BaseModelSchema
from ..models import db_user as U


class UserSchema(BaseModelSchema):

    class Meta:
        model = U.User
        exclude = ('password',)