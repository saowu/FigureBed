#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'


class FileMode(object):
    def __init__(self, file_name, network_path, md5_name=None, local_path=None):
        self.file_name = file_name
        self.md5_name = md5_name
        self.network_path = network_path
        self.local_path = local_path

    def __str__(self) -> str:
        return super().__str__()


def file2dict(obj):
    return {
        'name': obj.file_name,
        'path': obj.network_path
    }
