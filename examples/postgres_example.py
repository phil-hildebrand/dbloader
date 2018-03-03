#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import json
import os
import sys
import logging
from dbloader import dbloader as dbl

logger = logging.getLogger(__name__)

dbl.setup_logs('./dbloader.log', True)
options = dbl.load_config('./etc/load.yml')
if not options:
    exit(1)
for server in options['server']:
    if server['type'] == 'postgres':
        ldr = dbl.pg.PostgresLoader(server['name'], server['port'], server['user'], server['pass'], 'postgres')
        ldr.databases = ['pg_db_1', 'pg_db_2']
        ldr.tables = ['tbl_1', 'tbl_2']
        custom = server.get('custom', None)
        ldr.inserts = server.get('inserts', 50)
        ldr.deletes = server.get('deletes', 5)
        ldr.updates = server.get('updates', 5)
        ldr.selects = server.get('selects', 5)
        ldr.concurrency = server.get('concurrency', 5)
        ldr.itterations = server.get('itterations', 5)
        dbl.main(server['type'], ldr, custom)
