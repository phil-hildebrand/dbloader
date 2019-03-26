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

    def __init__(self, protocol, host, port): 
        '''
        Initialize a RiakLoader
        '''
        Loader.__init__(self)
        self.dbtype = 'Riak'
        self.databases = ['rb_1', 'rb_2', 'rb_3']
        self.protocol = protocol
        self.host = host
        self.port = port
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

    def insert(self, bucket, table=None, custom=None):
        '''
        Insert a single key/value
        '''

        logger.debug(' - Insert key %d', custom)
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            random_text = self.big_string(self.string_size)
            value = {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "custom": custom,
                     "concurrency": 1}
            kv = b.new(key=str(custom), data=value, content_type='application/json')
            result = kv.store()
            stored = b.get(kv.key)
            if len(stored.siblings) > 1:
                logger.info('{0} has siblings'.format(kv.key))

        except Exception:
            logger.exception('Unable to insert an object')
            return False
        return time.time() - start_time

    def update(self, bucket, table=None, custom=None):
        '''
        Update a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            kv = b.get(str(custom))
            if len(kv.siblings) > 1:
                logger.info('{0} has siblings: Skipping Update'.format(kv.key))
                logger.info('siblings: {0}'.format(kv.siblings))
            else:
                random_text = self.big_string(self.string_size)
                logger.info('siblings: {0}'.format(kv.siblings))
                if (kv.data):
                    kv.data['updated'] = start_time
                    kv.data['randString'] = random_text
                    result = kv.store()

        except Exception:
            logger.exception('Unable to update an object: (Key: %s)', custom)
            return False
        return time.time() - start_time

    def delete(self, bucket, table, custom=None):
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

    def select(self, bucket, table=None, custom=None):
        '''
        Select a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket)
            result = b.get(str(custom))
            if len(result.siblings) > 1:
                logger.info('{0} has siblings'.format(str(custom)))

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
        results = []

        if custom == self.inserts:
            min = 1
        else:
            min = custom - self.inserts + 1

        pool = Pool(self.concurrency)
        for bucket in self.databases:
                for ins in range(min, custom):
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
        for run in range(1, self.itterations):
            inserted = gevent.spawn(self.insert_some, run * self.inserts)
            updated = gevent.spawn(self.update_some, random.randint(1, self.inserts))
            deleted = gevent.spawn(self.delete_some,
                                   random.randint((run * self.inserts) - self.inserts + 1,
                                   run * self.inserts))
            selected = gevent.spawn(self.select_some, random.randint(1, self.inserts))
            gevent.wait(timeout=240)
            total_inserted += inserted.get()
            total_deleted += deleted.get()
            total_updated += updated.get()
            total_selected += selected.get()
        return(total_inserted, total_deleted, total_updated, total_selected)
