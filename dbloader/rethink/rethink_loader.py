#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import json
import rethinkdb as r
import time
import loader.loader as l
import logging

logger = logging.getLogger(__name__)


class RethinkLoader(l.Loader):

    def __init__(self):
        '''
        Initialize a RethinkLoader
        '''
        l.Loader.__init__(self)
        self.dbtype = 'RethinkDB'

    def get_connection(self, host, port):
        '''
        Get a rethink connection
        '''
        try:
            r.set_loop_type('gevent')
            self.conn = r.connect(self.host, self.port)

        except Exception:
            logger.exception('Unable to connect to database')
            return False
        return(self.conn)

    def create_if_not_exists(self, conn):
        '''
        If the databases or tables do not exist, create them
        '''
        if self.conn is None:
            self.conn = self.get_connection()

        try:
            for database in self.databases:
                dblist = r.db_list().run(self.conn)
                for table in self.tables:
                    tablist = r.db(database).table_list().run(self.conn)
                    if database not in dblist:
                        r.db_create(database).run(self.conn)
                        if table not in tablist:
                            r.db(database).table_create(table).run(self.conn)
                    else:
                        if table not in tablist:
                            r.db(database).table_create(table).run(self.conn)
            self.ready = True

        except Exception:
            logger.exception('Unable check and or setup databases/tables')
            self.ready = False
            exit(2)

        return True

    def insert(self, database, table):
        '''
        Insert a single record
        '''

        start_time = time.time()
        try:
            random_text = self.big_string(100)
            result = r.db(database).table(table).insert(
                {"type": "Load Test",
                 "randString": random_text,
                 "created": start_time,
                 "concurrency": 1},
                conflict="update").run(self.conn)

        except Exception:
            logger.exception('Unable to insert a record')
            return False
        return (time.time() - start_time)

    def delete(self, database, table):
        '''
        Delete a single record
        '''

        start_time = time.time()
        try:
            result = r.db(database).table(table).limit(1).delete().run(self.conn)

        except Exception:
            logger.exception('Unable to delete a record')
            raise Exception
        return (time.time() - start_time)

    def update(self, database, table):
        '''
        Update a single record
        '''

        start_time = time.time()
        try:
            result = r.db(database).table(table).limit(1).update({'type': 'LTU'}).run(self.conn)

        except Exception:
            logger.exception('Unable to update a record')
            raise Exception
        return (time.time() - start_time)

    def select(self, database, table):
        '''
        Select a single record
        '''

        start_time = time.time()
        try:
            result = r.db(database).table(table).limit(1).run(self.conn)

        except Exception:
            logger.exception('Unable to select a record')
            raise Exception
        return (time.time() - start_time)
