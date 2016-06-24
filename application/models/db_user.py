# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:07

from ._base import BaseModel
from ..core import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

user_role_table = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)

role_permission_table = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
)


class User(BaseModel):

    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    nickname = db.Column(db.String(50))
    password = db.Column(db.String(200))

    roles = db.relationship(
        'Role',
        secondary=user_role_table,
        backref='users',
    )

    def __setattr__(self, name, value):
        # Hash password when set it.
        if name == 'password':
            value = generate_password_hash(value)
        super(User, self).__setattr__(name, value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_roles(self, *roles):
        for role in roles:
            if not isinstance(role, Role):
                role_instance = Role.query.filter_by(flag=role['flag']).first()
            else:
                role_instance = role
            if role_instance not in self.roles:
                self.roles.append(role_instance)
        self.save()

    def remove_roles(self, *roles):
        for role in roles:
            if not isinstance(role, Role):
                role_instance = Role.query.filter_by(flag=role['flag']).first()
            else:
                role_instance = role
            if role_instance in self.roles:
                self.roles.remove(role_instance)
        self.save()


class Role(BaseModel):
    name = db.Column(db.String(120))
    flag = db.Column(db.String(120), unique=True)

    permissions = db.relationship(
        'Permission',
        secondary=role_permission_table,
        backref='roles',
    )

    def add_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                flag=permission['flag']
            ).first()
            if not existing_permission:
                existing_permission = Permission(
                    name=permission['name'],
                    flag=permission['flag'],
                    method=permission.get('method', 'get').upper(),
                )
                db.session.add(existing_permission)
                self.permissions.append(existing_permission)
        self.save()

    def remove_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                flag=permission['flag']
            ).first()
            if existing_permission and existing_permission in self.permissions:
                self.permissions.remove(existing_permission)
        self.save()

    @staticmethod
    def get_by_flag(flag):
        return Role.query.filter_by(flag=flag).first()


class Permission(BaseModel):
    name = db.Column(db.String(120))
    flag = db.Column(db.String(120))
    method = db.Column(db.String(10), default='GET')

    __table_args__ = (
        UniqueConstraint('flag', 'method', name='_flag_method_uc'),
    )

    @staticmethod
    def get_by_flag_and_method(flag, method='GET'):
        return Permission.query.filter_by(
            flag=flag,
            method=method.upper(),
        ).first()

    @staticmethod
    def get_by_flag(flag):
        return Permission.query.filter_by(
            flag=flag,
        ).all()