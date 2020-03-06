#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import hashlib
import os
import re
import time

from src.application import app


def init_dirs():
    '''
    初始化上传路径：UPLOAD_FOLDER
    :return:
    '''
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(r'' + app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    '''
    允许上传的文件类型
    :param filename: 文件名
    :return:true/false
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def get_file_stream(filename):
    '''
    得到文件流
    :param filename: 文件名
    :return: 文件流，文件类型
    '''
    listdir = os.listdir(app.config['UPLOAD_FOLDER'])
    for name in listdir:
        if re.match(filename + '.*', name):
            filename = name
    return [open(app.config['UPLOAD_FOLDER'] + filename, 'rb'), filename.rsplit('.', 1)[1]]


def get_name_md5(filename):
    '''
    对图片名称进行md5加密
    :param filename:
    :return:
    '''
    string = time.strftime("%Y-%m-%d-%H_%M_%S_", time.localtime(time.time())) + filename
    return hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()
