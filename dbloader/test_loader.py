
# -*- coding: utf-8 -*-

import json
import os
import sys
import logging
sys.path.append('../dbloader/')
sys.path.append('../')
sys.path.append('../dbloader/*')
import dbloader
import pytest

class TestDBLoader():

    def testLoader(self):
        '''We should be able to do a load run'''
        dbloader.setup_logs('./dbloader.log', True)
        options = dbloader.load_config('./etc/travis_load.yml')
        if options:
            server = options['server'][0]['name']
            type = options['server'][0]['type']
            port = options['server'][0]['port']
            user = options['server'][0]['user']
            passwd = options['server'][0]['pass']
        else:
            fail
        print ('setting host to %s' % server)
        dbloader.mongo_loader.host = server
        dbloader.mongo_loader.port = port
        dbloader.mongo_loader.inserts = 150
        dbloader.mongo_loader.deletes = 150
        dbloader.mongo_loader.concurrency = 10
        dbloader.main()
