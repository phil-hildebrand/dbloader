
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
            type = options['server'][0]['type']
            port = options['server'][0]['port']
            user = options['server'][0]['user']
            passwd = options['server'][0]['pass']
        else:
            fail
        dbl.logger.info('setting host to %s' % server)
        dbl.ml.host = server
        dbl.ml.port = port
        dbl.ml.inserts = 150
        dbl.ml.deletes = 150
        dbl.ml.concurrency = 10
        dbl.main()
