# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:03

from ..core import db
from ..utils.tool import get_now


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=get_now)

    def save(self):
        db.session.commit()

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.id)