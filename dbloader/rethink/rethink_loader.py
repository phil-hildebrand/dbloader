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
    '''
    A Loader class for load testing rethinkdb databases
    '''

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
        return self.conn

    def create_if_not_exists(self, conn, custom=None):
        '''
        If the databases or tables do not exist, create them
        '''
        if self.conn is None:
            self.conn = self.get_connection()

        try:
            if self.custom is not None:
                for crud in custom:
                    self.databases.append(crud['database'])
                    self.tables.append(crud['table'])
            for database in self.databases:
                for table in self.tables:
                    dblist = r.db_list().run(self.conn)
                    if database not in dblist:
                        r.db_create(database).run(self.conn)
                        tablist = r.db(database).table_list().run(self.conn)
                        if table not in tablist:
                            r.db(database).table_create(table).run(self.conn)
                    else:
                        tablist = r.db(database).table_list().run(self.conn)
                        if table not in tablist:
                            r.db(database).table_create(table).run(self.conn)
            self.ready = True

        except Exception:
            logger.exception('Unable check and or setup databases/tables')
            self.ready = False
            exit(2)

        return True

    def insert(self, database, table, custom=None):
        '''
        Insert a single record
        '''

        start_time = time.time()
        try:
            random_text = self.big_string(100)
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
                        result = r.db(database).table(table).insert(rdoc, conflict="update").run(self.conn) 
            else:
                result = r.db(database).table(table).insert(
                {"type": "Load Test",
                 "randString": random_text,
                 "created": start_time,
                 "concurrency": 1},
                conflict="update").run(self.conn)

        except Exception:
            logger.exception('Unable to insert a record')
            return False
        return time.time() - start_time

    def delete(self, database, table, custom=None):
        '''
        Delete a single record
        '''

        start_time = time.time()
        try:
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'delete':
                        records = crud['limit']
                        result = r.db(database).table(table).limit(records).delete().run(self.conn)
            else:
                result = r.db(database).table(table).limit(1).delete().run(self.conn)

        except Exception:
            logger.exception('Unable to delete a record')
            raise Exception
        return time.time() - start_time

    def update(self, database, table, custom=None):
        '''
        Update a single record
        '''

        start_time = time.time()
        try:
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'update':
                        doc = crud['update']
                        random_text = self.big_string(100)
                        for key, value in doc.items():
                            if value == "var_random":
                                doc[key] = random_text
                            if value == "var_created":
                                doc[key] = r.now()
                        records = crud['limit']
                        database = crud['database']
                        table = crud['table']
                        result = r.db(database).table(table).limit(records).update(doc).run(self.conn)
            else:
                result = r.db(database).table(table).limit(1).update({'type': 'LTU'}).run(self.conn)

        except Exception:
            logger.exception('Unable to update a record')
            raise Exception
        return time.time() - start_time

    def select(self, database, table, custom=None):
        '''
        Select a single record
        '''

        start_time = time.time()
        try:
            if custom is not None:
                for crud in custom:
                    if crud['ctype'] == 'select':
                        records = crud['limit']
                        database = crud['database']
                        table = crud['table']
                        result = r.db(database).table(table).limit(records).run(self.conn)
            else:
                result = r.db(database).table(table).limit(1).run(self.conn)

        except Exception:
            logger.exception('Unable to select a record')
            raise Exception
        return time.time() - start_time
