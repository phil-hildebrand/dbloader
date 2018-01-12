#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy_reg
import pymongo as m
from multiprocessing import Pool
import json
import random
import string
import sys
import time
import types

db_prefix = 'mongo_load_'
global test_collections
global host
global port
global inserts
global deletes
global updates
global selects
global concurrency

test_collections = ['ltc1', 'ltc2', 'ltc3']
inserts = 100
deletes = 100
updates = 100
selects = 100

def big_string(chars):
    return ''.join(random.choice(string.ascii_letters)
                   for _ in range(chars))

def get_connection(host, port):
    conn = m.MongoClient(host, port, connectTimeoutMS=2000, socketTimeoutMS=2000)
    return(conn)

def load_collection_docs(databases):
    '''We should be able to insert data into a collection for load tests'''
    load_db = databases
    total_insert = 0
    avg_insert = 0
    load_conn = get_connection(host, port)
    db = load_conn[load_db]

    for collections in test_collections:
        start_time = time.time()
        for ins in range(inserts):
            insert_time = time.time()
            my_text = big_string(100)
            try:
                x = db[collections].insert_one({"type": "Load Test",
                                                     "randString": my_text,
                                                     "created": insert_time,
                                                     "concurrency": 1})

            except Exception as e:
                print ('Load Insert Failed: (%s)' % e)

            inserted_time = time.time()
            avg_insert = (inserted_time - start_time) / (ins + 1)
        total_insert = inserted_time

        total_insert_duration = total_insert - start_time
        print('%s.%s - inserted %d in %0.2f seconds' % (databases,
                                                        collections,
                                                        ins,
                                                        total_insert_duration))
        print('  - Avg insert time: %0.4f seconds' % avg_insert)
    return (total_insert_duration)

def delete_collection_docs(databases):
    '''We should be able to delete a subset of documents from a collection'''

    delete_db = databases
    total_delete = 0
    avg_delete = 0
    deleted = 0
    del_conn = get_connection(host, port)
    db = del_conn[delete_db]

    for collections in test_collections:
        start_time = time.time()
        for delete in range(deletes):
            delete_time = time.time()
            try:
                result = db['mongo_collection'].delete_one({"randString": {"$exists": "true"}})
                deleted += result.deleted_count

            except Exception as e:
                print ('Delete Failed: (%s)' % e)

            deleted_time = time.time()
            avg_delete = (deleted_time - start_time) / (delete + 1)
        total_delete = deleted_time

        total_delete_duration = total_delete - start_time
        print('%s.%s - Deleted %d (%d reported) in %9.2f seconds' % (databases,
                                                                     collections,
                                                                     delete,
                                                                     deleted,
                                                                     total_delete_duration))
        print(' - Avg delete time: %9.4f seconds' % avg_delete)
    return (total_delete_duration)

def load_run():
    '''Run load test itteration'''
    print('Running Load Test')

    pool = Pool(processes=concurrency)
    start_time = time.time()
    test_dbs = []
    for run in range(concurrency):
        db = db_prefix + str(run)
        test_dbs.append(db)
    for load_duration in pool.imap_unordered(load_collection_docs, test_dbs):
        print('Load Run: %0.4f seconds' % load_duration)
    for delete_duration in pool.imap_unordered(delete_collection_docs, test_dbs):
        print('Delete Run : %0.4f seconds' % delete_duration)
    print('Current Run Time: %0.4f seconds' % (time.time() - start_time))
    print('Full Load Run Time: %0.4f seconds' % (time.time() - start_time))
