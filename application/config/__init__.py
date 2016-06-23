# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 10:57

import os


def load_config():
    mode = os.environ.get('MODE')

    try:
        if mode == "PRODUCTION":
            from .production import ProductionConfig
            return ProductionConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError:
        from .default import Config
        return Config