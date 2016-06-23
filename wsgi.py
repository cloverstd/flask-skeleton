# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 13:51

from application.factory import create_app

app = create_app()

if __name__ == '__main__':
    app.run()