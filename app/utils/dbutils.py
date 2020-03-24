#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import pymysql
from DBUtils.PooledDB import PooledDB


class DBUtil(object):
    __instance = None

    def __init__(self, host, port, database, user, password, ):
        # 数据库连接池
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset='utf8'
        )
        # 日志
        from .. import app
        app.logger.warning('PooledDB init success...')

    # 实现单例
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def create_conn_cursor(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def fetch_one(self, sql, args):
        '''
        查询一条数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def insert_many(self, sql, args):
        '''
        插入多条数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.create_conn_cursor()
        try:
            result = cursor.executemany(sql, args)
            conn.commit()
        except Exception as e:
            conn.rollback()
        cursor.close()
        conn.close()
        return result

    def delete_one(self, sql, args):
        '''
        删除一条数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.create_conn_cursor()
        try:
            result = cursor.execute(sql, args)
            conn.commit()
        except Exception as e:
            conn.rollback()
        cursor.close()
        conn.close()
        return result
