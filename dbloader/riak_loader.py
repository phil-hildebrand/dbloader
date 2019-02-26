#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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
        self.test_buckets = ['rb1', 'rb2', 'rb3']
        self.db_prefix = 'riak_load_'
        self.conn = None

    def get_connection(self):
        '''
        Get a riak connection
        '''
        try:
            self.conn = r.RiakClient(self.protocol,
                                     self.host,
                                     self.port)

        except Exception:
            logger.exception('Unable to connect to Riak')
            return False
        return

    def insert(self, bucket, bkey=None):
        '''
        Insert a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            random_text = Loader.big_string(100)
            value = {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "concurrency": 1}
            result = b.new(key=bkey, data=value, content_type='application/json')

        except Exception:
            logger.exception('Unable to insert an object')
            return False
        return time.time() - start_time

    def update(self, bucket, bkey=None):
        '''
        Update a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            random_text = Loader.big_string(100)
            value = {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "updated": start_time,
                     "concurrency": 1}
            result = b.set_data(key=bkey, data=value, content_type='application/json')

        except Exception:
            logger.exception('Unable to update an object')
            return False
        return time.time() - start_time

    def delete(self, bucket, bkey):
        '''
        Delete a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            result = b.delete(bkey)

        except Exception:
            logger.exception('Unable to delete key')
            raise Exception
        return time.time() - start_time

    def select(self, bucket, bkey):
        '''
        Select a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            result = b.get_data(bkey)

        except Exception:
            logger.exception('Unable to select key')
            raise Exception
        return time.time() - start_time
