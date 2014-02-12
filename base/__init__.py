# coding=utf-8
from flask import Blueprint


base = Blueprint(
    'base', __name__,
    template_folder='templates',
    url_prefix='/',
    static_folder='static'
)

from views import *
