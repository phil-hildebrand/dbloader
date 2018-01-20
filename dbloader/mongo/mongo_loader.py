#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import json
import pymongo as m
import time
import loader.loader as l
import logging

logger = logging.getLogger(__name__)


class MongoLoader(l.Loader):

    def __init__(self):
        '''
        Initialize a MongoLoader
        '''
        l.Loader.__init__(self)
        self.dbtype = 'MongoDB'
        self.test_collections = ['ltc1', 'ltc2', 'ltc3']
        self.db_prefix = 'mongo_load_'

    def get_connection(self, host, port):
        '''
        Get a mongo connection
        '''
        try:
            self.conn = m.MongoClient(self.host,
                                      self.port,
                                      connectTimeoutMS=2000,
                                      socketTimeoutMS=2000)

        except Exception:
            logger.exception('Unable to connect to database')
            return False
        return(self.conn)

    def insert(self, database, object):
        '''
        Insert a single record
        '''

        start_time = time.time()
        db = self.conn[database]
        try:
            random_text = self.big_string(100)
            result = db[object].insert_one({"type": "Load Test",
                                            "randString": random_text,
                                            "created": start_time,
                                            "concurrency": 1})

        except Exception:
            logger.exception('Unable to insert a record')
            return False
        return (time.time() - start_time)

    def delete(self, database, object):
        '''
        Delete a single record
        '''
        start_time = time.time()
        db = self.conn[database]
        try:
            result = db[object].delete_one({"randString": {"$exists": "true"}})

        except Exception:
            logger.exception('Unable to delete a record')
            raise Exception
        return (time.time() - start_time)
