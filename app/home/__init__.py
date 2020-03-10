#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

'''
Blueprint（static_url_path='/home/static'）====>/home/static
Flask（static_url_path='/static'）====>/static
必须配置，不配置默认为/static，将与Flask冲突，导致static失效
'''

from flask import Blueprint

home = Blueprint("home", __name__, template_folder='templates', static_folder='static', static_url_path='/home/static')

ACCEPT_TYPE = {"pdf": "application/pdf", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
               "png": "image/png", "csv": ".csv"}

import app.home.service
import app.home.views
