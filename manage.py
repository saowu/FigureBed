#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

from app import app

if __name__ == '__main__':
    # print(app.__dict__['url_map'])
    app.run()
