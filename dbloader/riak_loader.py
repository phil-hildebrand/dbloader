#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent.pool import Pool
from contextlib import closing
import json
import random
import riak as r
import time
from . import Loader
from . import logger


class RiakLoader(Loader):
    ''' Class for load testing Riak. '''

    def __init__(self, protocol, host='localhost', port=8098): 
        '''
        Initialize a RiakLoader
        '''
        super().__init__()
        self.dbtype = 'Riak'
        self.databases = ['rb_1', 'rb_2', 'rb_3']
        self.tables = []
        self.protocol = protocol
        self.host = host
        self.port = port
        self.conn = None
        self.timeout = 3600
        self.keyfile = "/tmp/truncate_keys"

    def get_connection(self):
        '''
        Get a riak connection
        '''
        try:
            self.conn = r.RiakClient(protocol=self.protocol,
                                     host=self.host,
                                     port=self.port)
            self.ready = True

        except Exception:
            logger.exception('Unable to connect to Riak')
            return False
        return

    def insert(self, bucket_name, table=None, custom=None):
        '''
        Insert a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket_name)
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

    def update(self, bucket_name, table=None, custom=None):
        '''
        Update a single key/value
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket_name)
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

    def delete(self, bucket_name, table, custom=None):
        '''
        Delete a single object
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket_name)
            obj = b.get(str(custom))
            r = obj.delete()

            logger.debug('Deleted %s from %s', custom, bucket_name)

        except Exception as e:
            logger.exception('Unable to delete key %s: %s', custom, e)
            raise Exception
        return time.time() - start_time

    def truncate(self, bucket_name, table=None, custom=None):
        '''
        Truncate a table/collection/bucket
        '''
        logger.debug('Truncating %s with %s', bucket_name, custom)
        tbucket = self.conn.bucket(bucket_name)
        keycount = 0
        get_one = 0
        deletes = []
        try:
            tpool = Pool(self.concurrency)
            with closing(self.conn.stream_keys(tbucket, self.timeout)) as keys:
                for key in keys:
                    keycount = keycount + 1
                    deletes.append(tpool.spawn(self.delete, bucket_name, None, key.strip()))
            tpool.join()
        except Exception as e:
            logger.error("Unable to stream keys from Riak for %s (%s)", bucket_name, e)
            pass

        logger.debug('Found %s keys in %s', keycount, bucket_name)
        logger.debug('Deleted %s keys from %s', len(deletes), bucket_name)

        return len(deletes)

    def select(self, bucket_name, table=None, custom=None):
        '''
        Select a single object
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        try:
            b = self.conn.bucket(bucket_name)
            result = b.get(str(custom))
            if len(result.siblings) > 1:
                logger.info('{0} has siblings'.format(str(custom)))

        except Exception:
            logger.exception('Unable to select key')
            raise Exception
        return time.time() - start_time

    def insert_some(self, custom=0):
        '''
        Load data into a bucket
        '''
        if not self.conn:
            self.get_connection()
        results = []

        if custom == self.inserts:
            min = 1
        else:
            min = max(0, custom - self.inserts + 1)

        pool = Pool(self.concurrency)
        for bucket_name in self.databases:
                for ins in range(min, custom):
                    results.append(pool.spawn(self.insert, bucket_name, None, ins))
                    if (ins % 10) == 0:
                        logger.debug(' - Inserted %d to %s', ins, bucket_name)
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
