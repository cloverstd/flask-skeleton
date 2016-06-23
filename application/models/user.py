# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:07

from ._base import BaseModel
from ..core import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):

    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    nickname = db.Column(db.String(50))
    password = db.Column(db.String(200))

    def __setattr__(self, name, value):
        # Hash password when set it.
        if name == 'password':
            value = generate_password_hash(value)
        super(User, self).__setattr__(name, value)

    def check_password(self, password):
        return check_password_hash(self.password, password)