#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import gevent
from gevent.pool import Pool
import random
import string
import sys
import time
from random import randint
from time import sleep


class Loader(object):

    def __init__(self):
        self.databases = ['dbl_1', 'dbl_2', 'dbl_3']
        self.objects = ['ltc1', 'ltc2', 'ltc3']

        self.concurrency = 20
        self.inserts = 100
        self.deletes = 100
        self.updates = 100
        self.selects = 100
        self.host = 'localhost'
        self.port = 3306

    def big_string(self, chars):
        return ''.join(random.choice(string.ascii_letters)
                       for _ in range(chars))

    def get_connection(self, host, port):
        try:
            self.conn = "connected"

        except Exception:
            print ('Unable to connect to database')
            return False
        return(self.conn)

    def insert(self, database, object):
        insert_time = time.time()
        try:
            random_text = self.big_string(100)
            result = 'insert data'

        except Exception:
            print ('Unable to insert a record')
            return False
        return (time.time() - insert_time)

    def delete(self, database, object):
        delete_time = time.time()
        try:
            result = 'delete data'

        except Exception:
            print ('Unable to delete a record')
            return False
        return (time.time() - delete_time)

    def insert_some(self):
        '''Load data into a table/collection/bucket'''

        load_conn = self.get_connection(self.host, self.port)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for object in self.objects:
                for ins in range(self.inserts):
                    results.append(pool.spawn(self.insert, database, object))
        pool.join()
        inserted = [r.get() for r in results]
        return (inserted)

    def delete_some(self):
        '''Delete a subset of data from a table/collection/bucket'''

        del_conn = self.get_connection(self.host, self.port)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for object in self.objects:
                for delete in range(self.deletes):
                    results.append(pool.spawn(self.delete, database, object))
        pool.join()
        deleted = [r.get() for r in results]
        return (deleted)

    def load_run(self):
        '''Run load test'''
        total_inserted = []
        total_deleted = []
        for run in range(1, self.itterations):
            inserted = gevent.spawn(self.insert_some)
            deleted = gevent.spawn(self.delete_some)
            gevent.wait(timeout=5)
            total_inserted += inserted.get()
            total_deleted += deleted.get()
        return(total_inserted, total_deleted)
