#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import logging
from context import dbloader as dbl
import pytest


class TestDBLoader():

    def testMongoLoader(self):
        '''We should be able to do a mongo load run'''
        dbl.setup_logs('./dbloader.log', True)
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
                ldr.inserts = 50
                ldr.deletes = 5
                ldr.updates = 5
                ldr.selects = 5
                ldr.concurrency = 10
                ldr.itterations = 2
                dbl.main(dbtype, ldr)

    def testRethinkLoader(self):
        '''We should be able to do a rethink load run'''
        dbl.setup_logs('./dbloader.log', True)
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
                ldr.port = port
                ldr.databases = ['rt_db_1', 'rt_db_2']
                ldr.tables = ['ltbl_1', 'ltbl_2']
                ldr.inserts = 50
                ldr.deletes = 5
                ldr.updates = 5
                ldr.selects = 5
                ldr.concurrency = 5
                ldr.itterations = 2
                dbl.main(dbtype, ldr)
