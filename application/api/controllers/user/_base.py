# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:14

from flask import Blueprint

bp = Blueprint(
    'user_show',
    __name__,
    url_prefix="/user",
)