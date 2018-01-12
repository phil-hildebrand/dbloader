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
        db_prefix = 'load_'
        test_objects = ['ltc1', 'ltc2', 'ltc3']

        concurrency = 20
        inserts = 100
        deletes = 100
        updates = 100
        selects = 100

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

    def insert_some(self, databases, objects):
        '''Load data into a table/collection/bucket'''

        load_conn = self.get_connection(host, port)
        results = []
    
        pool = Pool(concurrency)
        for database in databases:
            for object in objects:
                for ins in range(inserts):
                    results.append(pool.spawn(self.delete, database, object))
        pool.join()
        inserted = [ r.get() for r in results ]
        return (inserted)

    def delete_some(self, databases, objects):
        '''Delete a subset of data from a table/collection/bucket'''
    
        del_conn = self.get_connection(host, port)
        results = []
    
        pool = Pool(concurrency)
        for database in databases:
            for object in objects:
                for delete in range(deletes):
                    results.append(pool.spawn(self.delete, database, object))
        pool.join()
        deleted = [ r.get() for r in results ]
        return (deleted)

    def load_run(self, databases, objects, itterations):
        '''Run load test'''
        total_inserted = []
        total_deleted = []
        for run in range(1,itterations):
            inserted = gevent.spawn(self.insert_some, databases, objects)
            deleted = gevent.spawn(self.delete_some, databases, objects)
            gevent.wait()
            total_inserted.append(inserted.get())
            total_deleted.append(deleted.get())
        return(total_inserted, total_deleted)
