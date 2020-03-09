#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import logging
import os
import time


class UploadConfig(object):
    # images path
    UPLOAD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/myVolume/uploads/'
    # csv path
    RECORD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/myVolume/records/'


class DBConfig(object):
    # mysql
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DATABASE = 'figurebed'
    USER_NAME = 'root'
    PASSWORD = '123456'


class LogConfig(object):
    # logging
    LOG_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + "/myVolume/fb_logs/"
    LOG_FILENAME = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"
    LOG_LEVEL = logging.WARNING


class SchedulerConfig(object):
    # 定时任务
    JOBS = [
        {
            'id': 'clean_csv_files',
            'func': 'app:config.clean_csv_files',
            'trigger': 'interval',
            # 'days': 1,
            'minutes': 1,
        }
    ]


def clean_csv_files():
    '''
    清空csv文件
    :return:
    '''
    ls = os.listdir(UploadConfig.RECORD_FOLDER)
    for name in ls:
        os.remove(UploadConfig.RECORD_FOLDER + name)
        print('deleting-->', name)
