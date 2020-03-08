#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import logging
import os

# flask
import time

# images path
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/uploads/'
# csv path
RECORD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/records/'
# server run
SERVER_HOST = '127.0.0.1'
SERVER_PORT = '5000'
DEBUG = False
# mysql
DB_HOST = '118.89.237.69'
DB_PORT = '3306'
DATABASE = 'figurebed'
USER_NAME = 'root'
PASSWORD = '123456'
# logging
LOG_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + "/fb_logs/"
LOG_FILENAME = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"
LOG_LEVEL = logging.WARNING
