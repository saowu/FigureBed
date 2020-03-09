#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import json

from flask import request, url_for, abort, Response, render_template
from . import home
from . import service, ACCEPT_TYPE

from ..models import file2dict, FileMode


@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@home.route('/upload', methods=['POST'])
def upload_images():
    from app import app
    file_list = request.files.getlist('files')
    files = []
    # 获取image对象
    for file in file_list:
        old_filename = file.filename
        # 判断允许上传类型
        if file and service.allowed_file(old_filename):
            # 保存本地
            md5_string, new_filename = service.save_images(file)
            network_path = url_for('.index', _external=True) + 'image/' + md5_string
            local_path = app.config['UPLOAD_FOLDER'] + new_filename
            files.append(FileMode(old_filename, network_path, md5_string, local_path))
        else:
            files.append(FileMode(old_filename, "不符合文件类型"))
    # 插入数据库
    db_files = [_f for _f in files if not _f.md5_name is None]
    if not service.insert_files(db_files):
        abort(500)
    # 生成csv
    csv_path = service.list2csv(files)
    # 结果集
    result = {"fcsv": url_for('home.index', _external=True) + 'record/' + csv_path, "paths": files}
    return json.dumps(result, default=file2dict, )


@home.route('/image/<filename>', methods=['GET'])
def download_images(filename):
    image_info = service.get_image_stream(filename)
    if image_info is None:
        abort(404)
    return Response(image_info[0], mimetype=ACCEPT_TYPE[image_info[1]])


@home.route('/record/<filename>', methods=['GET'])
def download_records(filename):
    csv_info = service.get_record_stream(filename)
    if csv_info is None:
        abort(404)
    return Response(csv_info[0], mimetype=ACCEPT_TYPE[csv_info[1]])


@home.route('/removal/<filename>', methods=['GET'])
def remove_images(filename):
    is_remove = service.remove_image(filename)
    if is_remove is False:
        abort(404)
    return '<h1>Remove Success！</h1>'
