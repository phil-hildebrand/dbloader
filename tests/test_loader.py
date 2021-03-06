#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import logging
from dbloader import dbloader as dbl
import pytest

version = "{}".format(os.getenv('VERSION'))
postgres = os.getenv('POSTGRES_TEST')
mongo = os.getenv('MONGO_TEST')
rethink = os.getenv('RETHINK_TEST')
riak = os.getenv('RIAK_TEST')

logger = logging.getLogger(__name__)

class TestDBLoader():

    @pytest.mark.skipif((not mongo), reason="Not running Mongo")
    def testMongoLoader(self):
        '''We should be able to do a mongo load run'''
        dbl.setup_logs('./dbloader.log', False)
        options = dbl.load_config('./etc/travis_load.yml')
        if not options:
            fail
        for server in options['server']:
            node = server['name']
            dbtype = server['type']
            port = server['port']
            user = server['user']
            passwd = server['pass']
            if dbtype == 'mongo':
                ldr = dbl.ml.MongoLoader()
                ldr.host = node
                ldr.port = port
                ldr.databases = ['mongo_db_1', 'mongo_db_2']
                ldr.tables = ['ltbl_1', 'ltbl_2']
                ldr.inserts = server.get('inserts', 50)
                ldr.deletes = server.get('deletes', 5)
                ldr.updates = server.get('updates', 5)
                ldr.selects = server.get('selects', 5)
                ldr.concurrency = 10
                ldr.itterations = 2
                dbl.main(dbtype, ldr)

    @pytest.mark.skipif((not rethink), reason="Not running Rethink")
    def testRethinkLoader(self):
        '''We should be able to do a rethink load run'''
        dbl.setup_logs('./dbloader.log', False)
        options = dbl.load_config('./etc/travis_load.yml')
        if not options:
            fail
        for server in options['server']:
            node = server['name']
            dbtype = server['type']
            port = server['port']
            user = server['user']
            passwd = server['pass']
            if dbtype == 'rethink':
                ldr = dbl.rl.RethinkLoader()
                ldr.host = node
                ldr.custom = server['custom']
                ldr.port = server['port']
                ldr.databases = ['rt_db_1', 'rt_db_2']
                ldr.tables = ['ltbl_1', 'ltbl_2']
                ldr.inserts = server.get('inserts', 50)
                ldr.deletes = server.get('deletes', 5)
                ldr.updates = server.get('updates', 5)
                ldr.selects = server.get('selects', 5)
                ldr.concurrency = 5
                ldr.itterations = 2
                dbl.main(dbtype, ldr)

    @pytest.mark.skipif((not rethink), reason="Not running Postgres")
    def testPostgresLoader(self):
        '''We should be able to do a postgres load run'''
        dbl.setup_logs('./dbloader.log', False)
        options = dbl.load_config('./etc/travis_load.yml')
        if not options:
            fail
        for server in options['server']:
            if server['type'] == 'postgres':
                ldr = dbl.pg.PostgresLoader(server['name'], server['port'], server['user'], server['pass'], 'postgres')
                ldr.databases = ['pg_db_1', 'pg_db_2']
                ldr.tables = ['tbl_1', 'tbl_2']
                ldr.custom = server['custom']
                ldr.inserts = server.get('inserts', 50)
                ldr.deletes = server.get('deletes', 5)
                ldr.updates = server.get('updates', 5)
                ldr.selects = server.get('selects', 5)
                ldr.concurrency =  server.get('concurrency', 5)
                ldr.itterations = server.get('itterations', 5)
                dbl.main(server['type'], ldr)

    @pytest.mark.skipif((not riak), reason="Not running Riak")
    def testRiakLoader(self):
        '''We should be able to do a riak load run'''
        dbl.setup_logs('./dbloader.log', False)
        options = dbl.load_config('./etc/travis_load.yml')
        if not options:
            fail
        for server in options['server']:
            if server['type'] == 'riak':
                ldr = dbl.r.RiakLoader(server['protocol'], server['name'], server['port'])
                ldr.databases = ['riak_bucket_1', 'riak_bucket_2']
                ldr.protocol = server.get('protocol', 'http')
                ldr.host = server.get('host', '127.0.0.1')
                ldr.port = server.get('port', 8098)
                ldr.inserts = server.get('inserts', 50)
                ldr.deletes = server.get('deletes', 5)
                ldr.updates = server.get('updates', 5)
                ldr.selects = server.get('selects', 5)
                ldr.concurrency =  server.get('concurrency', 5)
                ldr.itterations = server.get('itterations', 5)
                dbl.main(server['type'], ldr)
