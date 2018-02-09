#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import rethinkdb as r
import time
from . import Loader
from . import logger


class RethinkLoader(Loader):
    '''
    A Loader class for load testing rethinkdb databases
    '''

    def __init__(self):
        '''
        Initialize a RethinkLoader
        '''
        Loader.__init__(self)
        self.dbtype = 'RethinkDB'
        self.version = r.__version__

    def get_connection(self):
        '''
        Get a rethink connection
        '''
        try:
            if self.version <= '2.3':
                old_conn = r.connect(self.host, self.port)
                return old_conn
            else:
                r.set_loop_type('gevent')
                self.conn = r.connect(self.host, self.port)

        except Exception as e:
            logger.exception('Unable to connect to database %s' % e)
            raise
        return self.conn

    def create_if_not_exists(self, custom=None):
        '''
        If the databases or tables do not exist, create them
        '''
        if self.version <= '2.3':
            conn = self.get_connection(self.host, self.port)
        else:
            if self.conn is None:
                self.conn = self.get_connection(self.host, self.port)
            conn = self.conn
        try:
            if custom is not None:
                for crud in custom:
                    self.databases.append(crud['database'])
                    self.tables.append(crud['table'])
            for database in self.databases:
                for table in self.tables:
                    dblist = r.db_list().run(conn)
                    if database not in dblist:
                        r.db_create(database).run(conn)
                        tablist = r.db(database).table_list().run(conn)
                        if table not in tablist:
                            r.db(database).table_create(table).run(conn)
                    else:
                        tablist = r.db(database).table_list().run(conn)
                        if table not in tablist:
                            r.db(database).table_create(table).run(conn)
            self.ready = True
            if self.version <= '2.3':
                conn.close()
                if self.conn:
                    self.conn.close()

        except Exception as e:
            logger.exception('Unable check and or setup databases/tables: %s' % e)
            self.ready = False
            exit(2)

        return True

    def insert(self, database, table, custom=None):
        '''
        Insert a single record
        '''

        start_time = time.time()
        try:
            if self.version <= '2.3':
                conn = self.get_connection(self.host, self.port)
            else:
                conn = self.conn
            random_text = Loader.big_string(100)
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'insert':
                        doc = crud['insert']
                        rdoc = json.loads(doc)
                        for key, value in rdoc.items():
                            if value == "var_random":
                                rdoc[key] = random_text
                            if value == "var_created":
                                rdoc[key] = r.now()
                        database = crud['database']
                        table = crud['table']
                        result = r.db(database).table(table).insert(rdoc, conflict="update").run(conn)
            else:
                result = r.db(database).table(table).insert(
                    {"type": "Load Test",
                     "randString": random_text,
                     "created": start_time,
                     "concurrency": 1},
                    conflict="update").run(conn)
            if self.version <= '2.3':
                conn.close()
                if self.conn:
                    self.conn.close()

        except Exception as e:
            logger.exception('Unable to insert a record: %s' % e)
            return False
        return time.time() - start_time

    def delete(self, database, table, custom=None):
        '''
        Delete a single record
        '''

        start_time = time.time()
        try:
            if self.version <= '2.3':
                conn = self.get_connection(self.host, self.port)
            else:
                conn = self.conn
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'delete':
                        records = crud['limit']
                        result = r.db(database).table(table).limit(records).delete().run(conn)
            else:
                result = r.db(database).table(table).limit(1).delete().run(conn)
            if self.version <= '2.3':
                conn.close()
                if self.conn:
                    self.conn.close()

        except Exception as e:
            logger.exception('Unable to delete a record %s ' % e)
            return False
        return time.time() - start_time

    def update(self, database, table, custom=None):
        '''
        Update a single record
        '''

        start_time = time.time()
        try:
            if self.version <= '2.3':
                conn = self.get_connection(self.host, self.port)
            else:
                conn = self.conn
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'update':
                        doc = crud['update']
                        random_text = Loader.big_string(100)
                        for key, value in doc.items():
                            if value == "var_random":
                                doc[key] = random_text
                            if value == "var_created":
                                doc[key] = r.now()
                        records = crud['limit']
                        database = crud['database']
                        table = crud['table']
                        result = r.db(database).table(table).limit(records).update(doc).run(conn)
            else:
                result = r.db(database).table(table).limit(1).update({'type': 'LTU'}).run(conn)
            if self.version <= '2.3':
                conn.close()
                if self.conn:
                    self.conn.close()

        except Exception as e:
            logger.exception('Unable to update a record %s' % e)
            return False
        return time.time() - start_time

    def select(self, database, table, custom=None):
        '''
        Select a single record
        '''

        start_time = time.time()
        results = []
        try:
            if self.version <= '2.3':
                conn = self.get_connection(self.host, self.port)
            else:
                conn = self.conn
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'select':
                        records = crud['limit']
                        database = crud['database']
                        table = crud['table']
                        result = r.db(database).table(table).limit(records).run(conn)
                        for record in result:
                            results.append(record)
            else:
                result = r.db(database).table(table).limit(1).run(conn)
                for record in result:
                    results.append(record)
            if self.version <= '2.3':
                conn.close()
                if self.conn:
                    self.conn.close()
            results = []

        except Exception as e:
            logger.exception('Unable to select a record %s' % e)
            results = []
            return False
        return time.time() - start_time
