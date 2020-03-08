#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import json
import logging
import os

from flask import Flask, url_for, render_template, request, Response, abort
from flask_apscheduler import APScheduler

from src import service, model, config

ACCEPT_TYPE = {"pdf": "application/pdf", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
               "png": "image/png", "csv": ".csv"}


def init_Flask():
    '''
    初始化Flask
    :return:
    '''
    _app = Flask('FigureBed')
    _app.config.from_object(config)
    # 创建image,csv,log目录
    if not os.path.exists(_app.config['UPLOAD_FOLDER']):
        os.makedirs(r'' + _app.config['UPLOAD_FOLDER'])
    if not os.path.exists(_app.config['RECORD_FOLDER']):
        os.makedirs(r'' + _app.config['RECORD_FOLDER'])
    if not os.path.exists(_app.config['LOG_FOLDER']):
        os.makedirs(r'' + _app.config['LOG_FOLDER'])
    # 初始化log
    log_file_str = _app.config['LOG_FOLDER'] + _app.config['LOG_FILENAME']
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler = logging.FileHandler(log_file_str, encoding='UTF-8')
    handler.setLevel(_app.config['LOG_LEVEL'])
    handler.setFormatter(log_formatter)
    _app.logger.addHandler(handler)
    return _app


app = init_Flask()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_images():
    try:
        file_list = request.files.getlist('files')
        files = []
        # 获取image对象
        for file in file_list:
            old_filename = file.filename
            # 判断允许上传类型
            if file and service.allowed_file(old_filename):
                # 保存本地
                md5_string, new_filename = service.save_images(file)
                network_path = url_for('index', _external=True) + 'image/' + md5_string
                local_path = app.config['UPLOAD_FOLDER'] + new_filename
                files.append(model.FileMode(old_filename, network_path, md5_string, local_path))
            else:
                files.append(model.FileMode(old_filename, "不符合文件类型"))
        # 生成csv
        csv_path = service.list2csv(files)
        # 插入数据库
        db_files = [_f for _f in files if not _f.md5_name is None]
        if not service.insert_files(db_files):
            abort(500)
        # 结果集
        result = {"fcsv": url_for('index', _external=True) + 'record/' + csv_path, "paths": files}
        return json.dumps(result, default=model.file2dict, )
    except Exception as e:
        app.logger.error('Upload Error:', e)


@app.route('/image/<filename>', methods=['GET'])
def download_images(filename):
    image_info = service.get_image_stream(filename)
    if image_info is None:
        abort(404)
    return Response(image_info[0], mimetype=ACCEPT_TYPE[image_info[1]])


@app.route('/record/<filename>', methods=['GET'])
def download_records(filename):
    csv_info = service.get_record_stream(filename)
    if csv_info is None:
        abort(404)
    return Response(csv_info[0], mimetype=ACCEPT_TYPE[csv_info[1]])


@app.route('/removal/<filename>', methods=['GET'])
def remove_images(filename):
    is_remove = service.remove_image(filename)
    if is_remove is False:
        abort(404)
    return '<h1>Remove Success！</h1>'


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=app.config['DEBUG'], host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
