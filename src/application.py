#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' src module '

__author__ = 'saowu'

import json, time, os
from flask import Flask, url_for, render_template, request, jsonify
from flask_cors import CORS

from src.file_mode import FileMode, file2dict

app = Flask('FigureBed')

app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.dirname(__file__)) + '/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

CORS(app, supports_credentials=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def update():
    getlist = request.files.getlist('files')
    files = []
    for file in getlist:
        if file and allowed_file(file.filename):
            now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            filename = file.filename
            name = str(now) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
            files.append(FileMode(filename, 'http://127.0.0.1:8000/upload/' + name))
    return json.dumps(files, default=file2dict, )


if __name__ == '__main__':
    app.run(debug=False, port='8000', host='127.0.0.1')
