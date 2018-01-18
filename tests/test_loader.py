#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
import logging
from context import dbloader as dbl
import pytest

class TestDBLoader():

    def testLoader(self):
        '''We should be able to do a load run'''
        dbl.setup_logs('./dbloader.log', True)
        options = dbl.load_config('./etc/travis_load.yml')
        if options:
            server = options['server'][0]['name']
            dbtype = options['server'][0]['type']
            port = options['server'][0]['port']
            user = options['server'][0]['user']
            passwd = options['server'][0]['pass']
        else:
            fail
        dbl.logger.info('setting host to %s' % server)
        if dbtype == 'rethink':
            dbl.logger.info('DB Type %s' % dbtype)
            ldr = dbl.rl.rethinkLoader()
            ldr.host = server
            ldr.port = port
            ldr.databases = ['mongo_db_1', 'mongo_db_2']
            ldr.tables = ['ltbl_1', 'ltbl_2']
        if dbtype == 'mongo':
            dbl.logger.info('DB Type %s' % dbtype)
            ldr = dbl.ml.mongoLoader()
            ldr.host = server
            ldr.port = port
            ldr.databases = ['rt_db_1', 'rt_db_2']
            ldr.tables = ['ltbl_1', 'ltbl_2']
        ldr.inserts = 50
        ldr.deletes = 5
        ldr.concurrency = 10
        ldr.itterations = 2
        dbl.main(dbtype, ldr)
