#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import json
import os
import sys
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './dbloader')))
import dbloader as dbl

logger = logging.getLogger(__name__)

dbl.setup_logs('./dbloader.log', True)
options = dbl.load_config('./etc/load.yml')
if not options:
    exit(1)
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
        ldr.concurrency =  server.get('concurrency', 5)
        ldr.itterations = server.get('itterations', 5)
        dbl.main(dbtype, ldr)
