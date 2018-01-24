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

logger = logging.getLogger(__name__)


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

        self.concurrency = 20
        self.inserts = 100
        self.deletes = 100
        self.updates = 100
        self.selects = 100
        self.host = 'localhost'
        self.port = 3306
        self.ready = False
        self.custom = None

    def big_string(self, chars):
        '''
        Build some randome data
        '''
        return ''.join(random.choice(string.ascii_letters)
                       for _ in range(chars))

    def get_connection(self, host, port):
        '''
        Get a connection to a database
        '''
        try:
            self.conn = "connected"

        except Exception:
            logger.exception('Unable to connect to database')
            return False
        return(self.conn)

    def create_if_not_exists(self, conn, custom=None):
        '''
        If the databases or tables do not exist, create them
        '''
        if self.conn is None:
            self.conn = "connected"

        try:
            for database in self.databases:
                for table in self.tables:
                    if database:
                        if table:
                            self.ready = True
                    else:
                        if table:
                            self.ready = True
            self.ready = True

        except Exception:
            logger.exception('Unable check and or setup databases/tables')
            self.ready = False
            exit(2)

        return True


    def insert(self, database, table, custom=None):
        '''
        Insert a record
        '''
        start_time = time.time()
        try:
            random_text = self.big_string(100)
            result = 'insert data'

        except Exception:
            logger.exception('Unable to insert a record')
            return False
        return (time.time() - start_time)

    def delete(self, database, table):
        '''
        Delete a record
        '''
        start_time = time.time()
        try:
            result = 'delete data'

        except Exception:
            logger.exception('Unable to delete a record')
            return False
        return (time.time() - start_time)

    def update(self, database, table):
        '''
        update a record
        '''
        start_time = time.time()
        try:
            result = 'update data'

        except Exception:
            logger.exception('Unable to update a record')
            return False
        return (time.time() - start_time)

    def select(self, database, table):
        '''
        select a record
        '''

        start_time = time.time()
        try:
            result = 'select data'

        except Exception:
            logger.exception('Unable to select a record')
            return False
        return (time.time() - start_time)

    def insert_some(self, custom=None):
        '''
        Load data into a table/collection/bucket
        '''

        self.conn = self.get_connection(self.host, self.port)
        if not self.ready:
            self.create_if_not_exists(self.conn, self.custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for ins in range(self.inserts):
                    results.append(pool.spawn(self.insert, database, table, custom))
        pool.join()
        inserted = [r.get() for r in results]
        return (inserted)

    def delete_some(self):
        '''
        Delete a subset of data from a table/collection/bucket
        '''

        self.conn = self.get_connection(self.host, self.port)
        if not self.ready:
            self.create_if_not_exists(self.conn, self.custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for delete in range(self.deletes):
                    results.append(pool.spawn(self.delete, database, table))
        pool.join()
        deleted = [r.get() for r in results]
        return (deleted)

    def update_some(self):
        '''
        Update a subset of data from a table/collection/bucket
        '''

        self.conn = self.get_connection(self.host, self.port)
        if not self.ready:
            self.create_if_not_exists(self.conn, self.custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for delete in range(self.updates):
                    results.append(pool.spawn(self.update, database, table))
        pool.join()
        updated = [r.get() for r in results]
        return (updated)

    def select_some(self):
        '''
        Select a subset of data from a table/collection/bucket
        '''

        self.conn = self.get_connection(self.host, self.port)
        if not self.ready:
            self.create_if_not_exists(self.conn, self.custom)
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            for table in self.tables:
                for delete in range(self.selects):
                    results.append(pool.spawn(self.select, database, table))
        pool.join()
        selected = [r.get() for r in results]
        return (selected)

    def load_run(self):
        '''
        Run load test
        '''

        total_inserted = []
        total_deleted = []
        total_updated = []
        total_selected = []
        logger.debug('Running full Load test')
        self.conn = self.get_connection(self.host, self.port)
        if not self.ready:
            self.create_if_not_exists(self.conn, self.custom)
        for run in range(1, self.itterations):
            inserted = gevent.spawn(self.insert_some(self.custom))
            deleted = gevent.spawn(self.delete_some)
            updated = gevent.spawn(self.update_some)
            selected = gevent.spawn(self.select_some)
            gevent.wait(timeout=5)
            total_inserted += inserted.get()
            total_deleted += deleted.get()
            total_updated += updated.get()
            total_selected += selected.get()
        return(total_inserted, total_deleted, total_updated, total_selected)
