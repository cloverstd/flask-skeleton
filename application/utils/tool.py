# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:04

import arrow
import glob
import os.path


def get_now(naive=True):
    """
    get now
    :param naive:
    :return:
    """
    now = arrow.now()
    if naive:
        return now.naive
    return now


def get_bp_controller(f, name, prefix="bp_"):
    """
    auto import modules
    :param f: __file__
    :param name: __name__
    :param prefix: default bp_
    :return:
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(f)))
    modules = map(lambda x: os.path.basename(x)[:-3], glob.glob(os.path.join(base_path, '{}*.py'.format(prefix))))
    map(lambda x: __import__("{}.{}".format(name, x)), modules)