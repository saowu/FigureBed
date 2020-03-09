#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

from flask import Blueprint

home = Blueprint("home", __name__, template_folder='../templates', static_folder='../static')

ACCEPT_TYPE = {"pdf": "application/pdf", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
               "png": "image/png", "csv": ".csv"}

import app.home.service
import app.home.views
