#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pymongo as m
import time
from . import Loader
from . import logger


class MongoLoader(Loader):
    ''' Class for load testing Mongo db. '''

    def __init__(self):
        '''
        Initialize a MongoLoader
        '''
        Loader.__init__(self)
        self.dbtype = 'MongoDB'
        self.test_collections = ['ltc1', 'ltc2', 'ltc3']
        self.db_prefix = 'mongo_load_'
        self.conn = None

    def get_connection(self):
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
        return

    def insert(self, database, collection, custom=None):
        '''
        Insert a single record
        '''

        start_time = time.time()
        if not self.conn:
            self.get_connection()
        db = self.conn[database]
        try:
            random_text = self.big_string()
            result = db[collection].insert_one({"type": "Load Test",
                                                "randString": random_text,
                                                "created": start_time,
                                                "concurrency": 1})

        except Exception:
            logger.exception('Unable to insert a record')
            return False
        return time.time() - start_time

    def delete(self, database, collection, custom=None):
        '''
        Delete a single record
        '''
        start_time = time.time()
        if not self.conn:
            self.get_connection()
        db = self.conn[database]
        try:
            result = db[collection].delete_one({"randString": {"$exists": "true"}})

        except Exception:
            logger.exception('Unable to delete a record')
            raise Exception
        return time.time() - start_time
