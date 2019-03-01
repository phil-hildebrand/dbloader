#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2 as p
import time
import random
from . import Loader
from . import logger
import os


class PostgresLoader(Loader):
    '''
    A Loader class for load testing postgresql databases
    '''
    def __init__(self, host, port, user, password, db):
        '''
        Initialize a Postgres Loader
        '''
        Loader.__init__(self)
        self.dbtype = 'Postgres'
        self.port = port
        self.host = host
        self.username = user
        self.password = password
        self.db = db
        self.role = 'DBA'

    def get_connection(self, dbname=None):
        '''
        Get a postgres db connection
        '''
        try:
            if dbname:
                conn = p.connect(dbname=dbname,
                                 user=self.username,
                                 password=self.password,
                                 host=self.host,
                                 port=self.port)
            else:
                conn = p.connect(dbname=self.db,
                                 user=self.username,
                                 password=self.password,
                                 host=self.host,
                                 port=self.port)
            conn.set_isolation_level(p.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            return conn
        except Exception as e:
            logger.exception('Unable to connect to database %s' % e)
            raise

    def check_and_create_db(self, db):
        ''' Check if db is present and create if not.'''
        try:
            conn = self.get_connection()
            exists = 0
            # check whether db exists
            check_db = "SELECT count(*) FROM pg_database WHERE datname='%s';" % db
            with conn.cursor() as cursor:
                cursor.execute(check_db)
                row = cursor.fetchone()
                if row is not None:
                    exists = int(row[0])
                # create if not
            if exists < 1:
                cr_db = 'create database %s;' % db
                with conn.cursor() as cursor:
                    cursor.execute("SET ROLE %s;" % self.role)
                    cursor.execute(cr_db)
                conn.close()
        except Exception as e:
            logger.error("Error while checking and creating db : %s" % e)
            raise

    def check_and_create_table(self, db, table, table_create):
        ''' Check if table is present in db and create if not.'''
        try:
            if not all([db, table]):
                logger.warn("No db or table given for creation")
                return False
            db_conn = self.get_connection(db)
            if not table_create:
                table_create = " id serial primary key, name varchar(20), cool_json json "
                logger.warn('table create script not found for %s using default: %s' % (table, table_create))
            cr_table = 'create table if not exists %s (%s) ;' % (table, table_create)
            with db_conn.cursor() as cursor:
                cursor.execute("SET ROLE %s;" % self.role)
                cursor.execute(cr_table)
            db_conn.close()
            return True
        except Exception as e:
            logger.error("Error while checking and creating table : %s" % e)
            raise

    def create_if_not_exists(self, custom=None):
        ''' Create table or db if they do not exist.'''
        try:
            for database in self.databases:
                for table in self.tables:
                    self.check_and_create_db(database)
                    self.check_and_create_table(database, table, '')
            if custom:
                for crud in custom:
                    db = crud['database']
                    table = crud['table']
                    table_create = crud.get('table_create_script', '')
                    self.check_and_create_db(db)
                    self.check_and_create_table(db, table, table_create)

            self.ready = True
        except Exception as e:
            logger.error("Error while checking and creating table : %s" % e)
            raise

    def insert(self, dbname, tablename, custom=None):
        ''' Insert a single record.'''
        start_time = time.time()
        try:
            if custom:
                for crud in custom:
                    if crud['ctype'] == 'insert':
                        data = dict(crud['insert'])
                        columns = ''
                        values = ''
                        for key, val in data.items():
                            columns = columns + str(key)
                            values = values + str(val)
                            if key != data.keys()[-1]:
                                columns = columns + ","
                                values = values + ","
                        database = crud['database']
                        table = crud['table']
                        db_conn = self.get_connection(database)
                        sql = 'insert into %s (%s) values ( %s );' % (table, columns, values)
                        with db_conn.cursor() as cursor:
                            cursor.execute("SET ROLE %s;" % self.role)
                            cursor.execute(sql)
                        db_conn.close()
            else:
                random_txt = self.big_string()
                self.string_size = self.string_size * 3
                random_json_string_data = self.big_string()
                self.string_size = self.string_size / 3
                ran_json = '{"name": "%s", "data": "%s"}' % (random_txt, random_json_string_data)
                sql = "insert into %s (name, cool_json) values ('%s', '%s');" % (tablename, random_txt, ran_json)
                db_conn = self.get_connection(dbname)
                with db_conn.cursor() as cursor:
                    cursor.execute("SET ROLE %s;" % self.role)
                    cursor.execute(sql)
                db_conn.close()
        except Exception as e:
            logger.error("Unable to insert a record: %s" % e)
            raise
        return time.time() - start_time

    def delete(self, dbname, tablename, custom=None):
        ''' Delete matching records. '''
        start_time = time.time()
        try:
            if custom:
                for crud in custom:
                    if crud['ctype'] == 'delete':
                        db = crud['database']
                        table = crud['table']
                        limit = crud['limit']
                        db_conn = self.get_connection(db)
                        sql = "delete from %s where id in (select id from %s LIMIT %d);" % (table, table, limit)
                        with db_conn.cursor() as cursor:
                            cursor.execute("SET ROLE %s;" % self.role)
                            cursor.execute(sql)
                        db_conn.close()
            else:
                db_conn = self.get_connection(dbname)
                # delete one record
                sql = "delete from %s where ctid in (select ctid from %s LIMIT 1);" % (tablename, tablename)
                with db_conn.cursor() as cursor:
                    cursor.execute("SET ROLE %s;" % self.role)
                    cursor.execute(sql)
                db_conn.close()
        except Exception as e:
            logger.error("Unable to delete a record: %s" % e)
            raise
        return time.time() - start_time

    def update(self, dbname, tablename, custom=None):
        ''' Update one records'''
        start_time = time.time()
        try:
            if custom:
                for crud in custom:
                    if crud['ctype'] == 'update':
                        db = crud['database']
                        table = crud['table']
                        update_val = crud['update']
                        column = crud['column']
                        columntype = crud['columntype']
                        db_conn = self.get_connection(db)
                        sql = "update %s set %s = cast( '%s' as %s ) where id in (select id from %s LIMIT 1);" % (table, column, update_val, columntype, table)
                        with db_conn.cursor() as cursor:
                            cursor.execute("SET ROLE %s;" % self.role)
                            cursor.execute(sql)
                        db_conn.close()
            else:
                db_conn = self.get_connection(dbname)
                rand_text = self.big_string()
                sql = "update %s set name = '%s' where id in (select id from %s LIMIT 1);" % (tablename, rand_text, tablename)
                with db_conn.cursor() as cursor:
                    cursor.execute("SET ROLE %s;" % self.role)
                    cursor.execute(sql)
                db_conn.close()
        except Exception as e:
            logger.error("Unable to update a record: %s" % e)
            raise
        return time.time() - start_time

    def select(self, dbname, tablename, custom=None):
        ''' select matching records'''
        start_time = time.time()
        try:
            if custom:
                for crud in custom:
                    if crud['ctype'] == 'select':
                        limit = crud['limit']
                        database = crud['database']
                        table = crud['table']
                        db_conn = self.get_connection(database)
                        sql = "select * from %s limit %d;" % (table, limit)
                        with db_conn.cursor() as cursor:
                            cursor.execute("SET ROLE %s;" % self.role)
                            cursor.execute(sql)
                        db_conn.close()
            else:
                sql = "select * from %s LIMIT 1;" % (tablename)
                db_conn = self.get_connection(dbname)
                with db_conn.cursor() as cursor:
                    cursor.execute("SET ROLE %s;" % self.role)
                    cursor.execute(sql)
                db_conn.close()
        except Exception as e:
            logger.error("Unable to select a record: %s" % e)
            raise
        return time.time() - start_time
