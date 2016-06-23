#!/usr/bin/env python
# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.factory import create_app
from application.core import db

app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-h', '--host', dest="host", default="0.0.0.0", type=str)
@manager.option('-p', '--port', dest="port", default=8080, type=int)
def run(host, port):
    from wsgi import application
    from werkzeug.serving import run_simple
    run_simple(host, port, application, use_reloader=True, use_debugger=True)

if __name__ == '__main__':
    manager.run()
