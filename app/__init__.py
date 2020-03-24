#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import logging
import os

from flask import Flask

from app import config
from app.config import UploadConfig, DBConfig, SchedulerConfig, LogConfig
from app.home import home as home_blueprint
from app.utils import dbutils
from app.utils.apsutils import init_scheduler

app = Flask("FigureBed")

app.debug = False

app.config.from_object(UploadConfig())
app.config.from_object(DBConfig())
app.config.from_object(SchedulerConfig())
app.config.from_object(LogConfig())

# 注册
app.register_blueprint(home_blueprint)

# 初始化log
log_file_str = app.config['LOG_FOLDER'] + app.config['LOG_FILENAME']
log_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler = logging.FileHandler(log_file_str, encoding='UTF-8')
handler.setLevel(logging.WARNING)
handler.setFormatter(log_formatter)
app.logger.addHandler(handler)

# 初始化数据库连接池
db = dbutils.DBUtil(app.config['DB_HOST'], app.config['DB_PORT'], app.config['DATABASE'], app.config['USER_NAME'],
                    app.config['PASSWORD'])

# 创建image,csv,log目录
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(r'' + app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['RECORD_FOLDER']):
    os.makedirs(r'' + app.config['RECORD_FOLDER'])
if not os.path.exists(app.config['LOG_FOLDER']):
    os.makedirs(r'' + app.config['LOG_FOLDER'])

# 定时任务
init_scheduler(app)
