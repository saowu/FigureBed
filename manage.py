#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

from app import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
