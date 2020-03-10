#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

from app import app

'''
 <Rule '/' (HEAD, GET, OPTIONS) -> home.index>,
 <Rule '/upload' (POST, OPTIONS) -> home.upload_images>,
 <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/home/static/<filename>' (HEAD, GET, OPTIONS) -> home.static>,
 <Rule '/removal/<filename>' (HEAD, GET, OPTIONS) -> home.remove_images>,
 <Rule '/record/<filename>' (HEAD, GET, OPTIONS) -> home.download_records>,
 <Rule '/image/<filename>' (HEAD, GET, OPTIONS) -> home.download_images>
'''
if __name__ == '__main__':
    # print(app.__dict__['url_map'])
    app.run()
