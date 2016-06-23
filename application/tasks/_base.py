# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:50

from application.factory import create_celery_app

celery = create_celery_app()


@celery.task
def say_hello(n=10):
    import time
    for i in xrange(n):
        print "say hello", i
        time.sleep(1)
