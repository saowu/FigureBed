#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import logging
import os
import time


class UploadConfig(object):
    # 外网ip和端口（如果添加了nginx代理，需要改成nginx的对外端口）
    IP = "http://127.0.0.1:8000/"
    # images path
    UPLOAD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/myDataVolume/uploads/'
    # csv path
    RECORD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/myDataVolume/records/'


class DBConfig(object):
    # mysql Docker部署可填宿主机内网ip
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DATABASE = 'figurebed'
    USER_NAME = 'root'
    PASSWORD = '123456'


class LogConfig(object):
    # logging
    LOG_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + "/myDataVolume/fb_logs/"
    LOG_FILENAME = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"
    LOG_LEVEL = logging.WARNING


class SchedulerConfig(object):
    # 定时任务
    JOBS = [
        {
            'id': 'clean_csv_files',
            'func': 'app:utils.apsutils.clean_csv_files',
            'trigger': 'interval',
            'days': 1,
            # 'seconds': 20,
        }
    ]
    SCHEDULER_API_ENABLED = True
