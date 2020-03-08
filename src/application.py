#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import os, json
from flask import Flask, url_for, render_template, request, Response, abort
from src import service, model, dbutils

app = Flask('FigureBed')
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.dirname(__file__)) + '/uploads/'
app.config['RECORD_FOLDER'] = os.path.dirname(os.path.dirname(__file__)) + '/records/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# 初始化数据库连接池
db = dbutils.DBUtil("127.0.0.1", 3306, "root", "123456", "figurebed")

accept_type = {"pdf": "application/pdf", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
               "png": "image/png", "csv": ".csv"}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# 有待抽取服务
@app.route('/upload', methods=['POST'])
def upload_images():
    try:
        file_list = request.files.getlist('files')
        files = []
        # 存储image
        for file in file_list:
            old_filename = file.filename
            if file and service.allowed_file(old_filename):
                md5_string = service.get_name_md5(old_filename.rsplit('.', 1)[0])
                new_filename = md5_string + "." + old_filename.rsplit('.', 1)[1]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                files.append(
                    model.FileMode(old_filename, md5_string, url_for('index', _external=True) + 'image/' + md5_string,
                                   app.config['UPLOAD_FOLDER'] + new_filename))
            else:
                files.append(model.FileMode(old_filename, "None", "不符合文件类型"))
        # 生成csv
        csv_path = service.list2csv(files)
        # 插入数据库
        if not service.insert_files(files):
            print("insert error:", csv_path)
        # 结果集
        result = {"fcsv": url_for('index', _external=True) + 'record/' + csv_path, "paths": files}
        return json.dumps(result, default=model.file2dict, )
    except Exception as e:
        print('Upload Error:', e)
        abort(500)


@app.route('/image/<filename>', methods=['GET'])
def download_images(filename):
    image_info = service.get_image_stream(filename)
    if image_info is None:
        abort(404)
    return Response(image_info[0], mimetype=accept_type[image_info[1]])


@app.route('/record/<filename>', methods=['GET'])
def download_records(filename):
    csv_info = service.get_record_stream(filename)
    if csv_info is None:
        abort(404)
    return Response(csv_info[0], mimetype=accept_type[csv_info[1]])


@app.route('/removal/<filename>', methods=['GET'])
def remove_images(filename):
    is_remove = service.remove_image(filename)
    if is_remove is False:
        abort(404)
    return '<h1>Remove Success！</h1>'


if __name__ == '__main__':
    service.init_dirs()
    app.run(debug=False, port='8000', host='127.0.0.1')
