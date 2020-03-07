#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import hashlib
import os
import re
import time
import pandas as pd

from src.application import app


def init_dirs():
    '''
    初始化上传路径：UPLOAD_FOLDER，RECORD_FOLDER
    :return:
    '''
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(r'' + app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['RECORD_FOLDER']):
        os.makedirs(r'' + app.config['RECORD_FOLDER'])


def allowed_file(filename):
    '''
    允许上传的文件类型
    :param filename: 文件名
    :return:true/false
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def get_image_stream(filename):
    '''
    得到image文件流
    :param filename: 文件名
    :return: 文件流，文件类型
    '''
    listdir = os.listdir(app.config['UPLOAD_FOLDER'])
    for name in listdir:
        if re.match(r'^' + filename + '\.(png|jpg|jpeg|gif|pdf)$', name):
            filename = name
            break
    if filename in listdir:
        return [open(app.config['UPLOAD_FOLDER'] + filename, 'rb'), filename.rsplit('.', 1)[1]]
    else:
        pass


def get_record_stream(filename):
    '''
    得到csv文件流
    :param filename: 文件名
    :return: 文件流，文件类型
    '''
    listdir = os.listdir(app.config['RECORD_FOLDER'])
    for _name in listdir:
        if re.match(r'^' + filename + '\.(csv)$', _name):
            filename = _name
            break
    if filename in listdir:
        return [open(app.config['RECORD_FOLDER'] + filename, 'rb'), filename.rsplit('.', 1)[1]]
    else:
        print(filename)
        pass


def get_name_md5(filename):
    '''
    对图片名称进行md5加密
    :param filename:
    :return: md5 string
    '''
    _string = time.strftime("%Y-%m-%d-%H_%M_%S_", time.localtime(time.time())) + filename
    return hashlib.md5(_string.encode(encoding='UTF-8')).hexdigest()


def list2csv(file_list):
    '''
    生成csv文件
    :param file_list: 数据
    :return: 保存路径
    '''
    _data = []
    for _file in file_list:
        _data.append({"file": _file.name, "path": _file.path})
    frame_data = pd.DataFrame(columns=["file", "path"], data=_data)
    csv_name = get_name_md5("record")
    csv_path = app.config['RECORD_FOLDER'] + csv_name + ".csv"
    frame_data.to_csv(csv_path)
    return csv_name
