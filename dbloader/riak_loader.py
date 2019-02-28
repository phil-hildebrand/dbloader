#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent.pool import Pool
import json
import random
import riak as r
import time
from . import Loader
from . import logger


class RiakLoader(Loader):
    ''' Class for load testing Riak. '''

    def __init__(self):
        '''
        Initialize a RiakLoader
        '''
        Loader.__init__(self)
        self.dbtype = 'Riak'
        self.buckets = ['rb_1', 'rb_2', 'rb_3']
        self.db_prefix = 'riak_load_'
        self.conn = None

    def get_connection(self):
        '''
        Get a riak connection
        '''
        try:
            self.conn = r.RiakClient(protocol=self.protocol,
                                     host=self.host,
                                     port=self.port)

        except Exception:
            logger.exception('Unable to connect to Riak')
            return False
        return

    def insert(self, bucket, bkey=None, custom=None):
        '''
        Insert a single key/value
        '''

        logger.debug(' - Insert key %d', custom)
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            random_text = Loader.big_string(100)
            value = {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "custom": custom,
                     "concurrency": 1}
            kv = b.new(key=str(custom), data=value, content_type='application/json')
            result = kv.store()
            stored = b.get(kv.key)

        except Exception:
            logger.exception('Unable to insert an object')
            return False
        logger.debug(' - Inserted %s (%s)', result.key, kv.data)
        logger.debug(' - Saved! (%s)', stored.data)
        return time.time() - start_time

    def update(self, bucket, bkey=None, custom=None):
        '''
        Update a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            kv = b.get(str(custom))
            random_text = Loader.big_string(100)
            value = {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "updated": start_time,
                     "concurrency": 1}
            kv.data = value
            result = kv.store()

        except Exception:
            logger.exception('Unable to update an object')
            return False
        return time.time() - start_time

    def delete(self, bucket, bkey, custom=None):
        '''
        Delete a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            result = b.delete(str(custom))

        except Exception:
            logger.exception('Unable to delete key')
            raise Exception
        return time.time() - start_time

    def select(self, bucket, bkey, custom=None):
        '''
        Select a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            result = b.get(str(custom))

        except Exception:
            logger.exception('Unable to select key')
            raise Exception
        return time.time() - start_time

    def insert_some(self, custom=None):
        '''
        Load data into a bucket
        '''
        if not self.conn:
            self.get_connection()
        if not self.ready:
            self.create_if_not_exists(custom)
        results = []

        pool = Pool(self.concurrency)
        for bucket in self.buckets:
                for ins in range(self.inserts):
                    results.append(pool.spawn(self.insert, bucket, None, ins))
        pool.join()
        inserted = [r.get() for r in results]
        return inserted

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
            inserted = gevent.spawn(self.insert_some, self.itterations * self.inserts)
            updated = gevent.spawn(self.update_some, random.randint(1, self.inserts))
            deleted = gevent.spawn(self.delete_some,
                                   random.randint((self.itterations * self.inserts) - self.inserts + 1,
                                   self.itterations * self.inserts))
            selected = gevent.spawn(self.select_some, random.randint(1, self.inserts))
            gevent.wait(timeout=240)
            total_inserted += inserted.get()
            total_deleted += deleted.get()
            total_updated += updated.get()
            total_selected += selected.get()
        return(total_inserted, total_deleted, total_updated, total_selected)