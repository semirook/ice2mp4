# coding=utf-8
from flask.ext.wtf import Form
from wtforms import (
    FileField,
)


class SubmitForm(Form):
    video = FileField('Video File')
