#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import os, json
from flask import Flask, url_for, render_template, request, Response
from src import utils, mode

app = Flask('FigureBed')
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.dirname(__file__)) + '/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

accept_type = {"pdf": "application/pdf", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
               "png": "image/png"}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_images():
    file_list = request.files.getlist('files')
    files = []
    for file in file_list:
        old_filename = file.filename
        if file and utils.allowed_file(old_filename):
            md5_string = utils.get_name_md5(old_filename.rsplit('.', 1)[0])
            new_filename = md5_string + "." + old_filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            files.append(mode.FileMode(old_filename, url_for('index', _external=True) + 'image/' + md5_string))
        else:
            files.append(mode.FileMode(old_filename, "不符合文件类型"))
    return json.dumps(files, default=mode.file2dict, )


@app.route('/image/<filename>', methods=['GET'])
def download_images(filename):
    image_info = utils.get_file_stream(filename)
    return Response(image_info[0], mimetype=accept_type[image_info[1]])


if __name__ == '__main__':
    utils.init_dirs()
    app.run(debug=False, port='8000', host='127.0.0.1')
