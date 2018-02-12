#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import gevent
from gevent.pool import Pool
import random
import string
import time
import logging

logger = logging.getLogger("dbloader")


class Loader(object):
    '''
    A class for load testing databases
    '''

    def __init__(self):
        '''
        Initialize a Loader
        '''
        self.databases = ['dbl_1', 'dbl_2', 'dbl_3']
        self.tables = ['ltc1', 'ltc2', 'ltc3']

        self.itterations = 1
        self.concurrency = 20
        self.inserts = 100
        self.deletes = 100
        self.updates = 100
        self.selects = 100
        self.host = 'localhost'
        self.port = 3306
        self.ready = False
        self.conn = None
        # self.custom = None

    @staticmethod
    def big_string(chars):
        '''
        Build some random data
        '''
        return ''.join(random.choice(string.ascii_letters)
                       for _ in range(chars))

    def get_connection(self):
        ''' Invoked everytime a new connection is needed. '''
        self.conn = True
        return

    def create_if_not_exists(self, custom=None):
        ''' Invoked to create databases or tables that do not exist'''
        self.ready = True
        return

    def insert(self, database, table, custom=None):
        '''
        Insert a record
        '''
        return time.time()

    def delete(self, database, table, custom=None):
        '''
        Delete a record
        '''
        return time.time()

    def update(self, database, table, custom=None):
        '''
        update a record
        '''
        return time.time()

    def select(self, database, table, custom=None):
        '''
        select a set of records.
        '''
        return time.time()

    def insert_some(self, custom=None):
        '''
        Load data into a table/collection/bucket
        '''
        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for ins in range(self.inserts):
                    results.append(pool.spawn(self.insert, database, table, custom))
        pool.join()
        inserted = [r.get() for r in results]
        return inserted

    def delete_some(self, custom=None):
        '''
        Delete a subset of data from a table/collection/bucket
        '''
        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for delete in range(self.deletes):
                    results.append(pool.spawn(self.delete, database, table, custom))
        pool.join()
        deleted = [r.get() for r in results]
        return deleted

    def update_some(self, custom=None):
        '''
        Update a subset of data from a table/collection/bucket
        '''
        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for delete in range(self.updates):
                    results.append(pool.spawn(self.update, database, table, custom))
        pool.join()
        updated = [r.get() for r in results]
        return updated

    def select_some(self, custom=None):
        '''
        Select a subset of data from a table/collection/bucket
        '''

        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for select in range(self.selects):
                    results.append(pool.spawn(self.select, database, table, custom))
        pool.join()
        selected = [r.get() for r in results]
        return selected

    def load_run(self, custom=None):
        '''
        Run load test
        '''

        total_inserted = []
        total_deleted = []
        total_updated = []
        total_selected = []
        logger.debug('Running full Load test')
        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        for run in range(1, self.itterations):
            inserted = gevent.spawn(self.insert_some, custom)
            deleted = gevent.spawn(self.delete_some, custom)
            updated = gevent.spawn(self.update_some, custom)
            selected = gevent.spawn(self.select_some, custom)
            gevent.wait(timeout=240)
            total_inserted += inserted.get()
            total_deleted += deleted.get()
            total_updated += updated.get()
            total_selected += selected.get()
        return(total_inserted, total_deleted, total_updated, total_selected)
