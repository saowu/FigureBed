#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import atexit
import fcntl
import os

from flask_apscheduler import APScheduler


def clean_csv_files():
    '''
    清空csv文件
    :return:
    '''
    from app import app
    ls = os.listdir(app.config["RECORD_FOLDER"])
    for name in ls:
        os.remove(app.config["RECORD_FOLDER"] + name)
    app.logger.warning("pid:", os.getpid(), "scheduler-clean_csv_files")


def init_scheduler(app):
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        from .. import app
        app.logger.warning('scheduler init success...')
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)
