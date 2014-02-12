# coding=utf-8
from helpers import AppFactory
from settings import DevelopmentConfig

app = AppFactory(DevelopmentConfig).get_app(__name__)
