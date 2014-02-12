# coding=utf-8
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "MY_VERY_SECRET_KEY"
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_PATH = os.path.join(ROOT_PATH, 'uploads')
    ALLOWED_MEDIA_EXTENSIONS = {
        '.3gp',
        '.avi',
        '.divx',
        '.flv',
        '.m4v',
        '.mkv',
        '.mov',
        '.mpeg',
        '.mpg',
        '.ogm',
        '.wmv',
    }

    BLUEPRINTS = ['base.base']


class DevelopmentConfig(BaseConfig):
    DEBUG = True
