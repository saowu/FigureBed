#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'


class FileMode(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self) -> str:
        return super().__str__()


def file2dict(obj):
    return {
        'name': obj.name,
        'path': obj.path
    }
