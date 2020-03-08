#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import hashlib
import os
import time
import pandas as pd

from src import dbutils
from src.application import app

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# 初始化数据库连接池
db = dbutils.DBUtil(app.config['DB_HOST'], app.config['DB_PORT'], app.config['DATABASE'], app.config['USER_NAME'],
                    app.config['PASSWORD'])


def allowed_file(filename):
    '''
    允许上传的文件类型
    :param filename: 文件名
    :return:true/false
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_images(file):
    '''
    保存image文件
    :param file: image
    :return:
    '''
    old_filename = file.filename
    md5_string = get_name_md5(old_filename.rsplit('.', 1)[0])
    new_filename = md5_string + "." + old_filename.rsplit('.', 1)[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return md5_string, new_filename


def get_image_stream(filename):
    '''
    得到image文件流
    :param filename: 文件名
    :return: 文件流，文件类型
    '''
    sql = "select * from t_files where name = %s;"
    file_model = db.fetch_one(sql, filename)
    if not file_model is None:
        return [open(file_model["path"], 'rb'), file_model["type"]]
    else:
        pass


def get_record_stream(filename):
    '''
    得到csv文件流
    :param filename: 文件名
    :return: 文件流，文件类型
    '''
    listdir = os.listdir(app.config['RECORD_FOLDER'])
    csv_ = filename + ".csv"
    if csv_ in listdir:
        return [open(app.config['RECORD_FOLDER'] + csv_, 'rb'), 'csv']
    else:
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
        _data.append(get_link_dict(_file))
    frame_data = pd.DataFrame(columns=["file", "link", "markdown", "html", "bbcode", "removal"], data=_data)
    csv_name = get_name_md5("record")
    csv_path = app.config['RECORD_FOLDER'] + csv_name + ".csv"
    frame_data.to_csv(csv_path)
    return csv_name


def get_link_dict(_file):
    '''
    构建各种链接
    :param _file: file_mode
    :return: dict
    '''
    _markdown = '![{0}]({1})'.format(_file.file_name, _file.network_path)
    _bbcode = '[url={0}][img]{1}[/img][/url]'.format(_file.network_path, _file.network_path)
    _html = '<a href="{0}" target="_blank"><img src="{1}"></a>'.format(_file.network_path, _file.network_path)
    _removal = _file.network_path.replace('image', 'removal')

    return {"file": _file.file_name, "link": _file.network_path, "markdown": _markdown, "html": _html,
            "bbcode": _bbcode,
            "removal": _removal}


def remove_image(filename):
    '''
    删除文件
    :param filename: 文件名
    :return: True/False
    '''
    sql_d = "DELETE FROM t_files where name = %s;"
    sql_s = "select * from t_files where name = %s;"
    file_model = db.fetch_one(sql_s, filename)
    if not file_model is None:
        try:
            os.remove(file_model["path"])
        except OSError as e:
            app.logger.error("remove_image Error:", e)
        if db.delete_one(sql_d, filename) == 1:
            return True
    else:
        return False


def insert_files(files):
    '''
    多条插入数据库
    :param files:
    :return:
    '''
    data = []
    for _file in files:
        data.append((_file.md5_name, _file.local_path, _file.file_name.rsplit('.', 1)[1]))
    sql = "INSERT INTO t_files (name,path,type) VALUES (%s,%s,%s);"
    try:
        result = db.insert_many(sql, data)
        if result == len(files):
            return True
        else:
            return False
    except Exception as e:
        app.logger.error("insert_files Error:", e)
