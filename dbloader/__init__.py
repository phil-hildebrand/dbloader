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


class Cleaner(object):
    '''
    A class for cleaning up databases after a load test
    '''
    # pylint: disable=too-many-instance-attributes


    def __init__(self):
        '''
        Initialize a cleaner
        '''
        self.databases = ['dbl_1', 'dbl_2', 'dbl_3']
        self.tables = ['ltc1', 'ltc2', 'ltc3']

        self.concurrency = 20
        self.host = 'localhost'
        self.port = 3306
        self.ready = False
        self.conn = None
        self.deletes = 0

    def get_connection(self):
        ''' Invoked everytime a new connection is needed. '''
        self.conn = True
        return

    def drop_if_exists(self, custom=None):
        ''' Invoked to drop databases or tables that exist'''
        self.ready = True
        logger.debug('Dropping %s (%s)', self.databases, custom)
        logger.debug('Dropping %s (%s)', self.tables, custom)
        return

    def delete(self, database, table=None, custom=None):
        '''
        Delete a record
        '''
        logger.debug('Deleting from %s.%s with %s', database, table, custom)
        return time.time()

    def truncate(self, database, table=None, custom=None):
        '''
        Truncate a table/collection/bucket
        '''
        logger.debug('Truncating %s.%s with %s', database, table, custom)
        return time.time()

    def delete_some(self, custom=None):
        '''
        Delete a subset of data from a table/collection/bucket
        '''
        if not self.conn:
            self.get_connection()
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            if len(self.tables) > 0:
                for table in self.tables:
                    logger.debug('Deleting from %s.%s (%s)', database, table, custom)
                    for delete in range(self.deletes):
                        results.append(pool.spawn(self.delete, database, table, custom))
            else:
                logger.debug('Deleting from %s (%s)', database, custom)
                for delete in range(self.deletes):
                    results.append(pool.spawn(self.delete, database, None, custom))
        pool.join()
        deleted = [r.get() for r in results]
        return deleted

    def delete_all(self, custom="truncate table"):
        '''
        Delete a all data from a database/table/collection
         but don't actually drop the database(s)/table(s)/collection(s)
        '''
        logger.debug(' - delete_all(%s)', custom)
        if not self.conn:
            self.get_connection()
        results = []

        pool = Pool(self.concurrency)
        for database in self.databases:
            if len(self.tables) > 0:
                for table in self.tables:
                    custom = custom + "{0};".format(table)
                    logger.debug('Deleting everything! (%s.%s :%s)', database, table, custom)
                    results.append(pool.spawn(self.truncate, database, table, custom))
            else:
                logger.debug('Deleting everything! (%s :%s)', database, custom)
                results.append(pool.spawn(self.truncate, database, None, custom))
        pool.join()
        deleted = [r.get() for r in results]
        return deleted

    
class Loader(Cleaner):
    '''
    A class for load testing databases
    '''
    # pylint: disable=too-many-instance-attributes


    def __init__(self):
        '''
        Initialize a Loader
        '''
        super()

        self.string_size = 100
        self.itterations = 1
        self.inserts = 100
        self.deletes = 100
        self.updates = 100
        self.selects = 100
        logger.debug('Loader initialized')

    @staticmethod
    def big_string(size):
        '''
        Build some random data
        '''
        return ''.join(random.choice(string.ascii_letters)
                       for _ in range(size))

    def create_if_not_exists(self, custom=None):
        ''' Invoked to create databases or tables that do not exist'''
        logger.debug('Creating %s (%s)', self.databases, custom)
        self.ready = True
        return

    def insert(self, database, table, custom=None):
        '''
        Insert a record
        '''
        logger.debug('Inserting into %s.%s (%s)', database, table, custom)
        return time.time()

    def update(self, database, table, custom=None):
        '''
        update a record
        '''
        logger.debug('Updating %s.%s (%s)', database, table, custom)
        return time.time()

    def select(self, database, table, custom=None):
        '''
        select a set of records.
        '''
        logger.debug('Selecting from %s.%s (%s)', database, table, custom)
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
                for update in range(self.updates):
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
