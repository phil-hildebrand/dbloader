#!/usr/bin/env python
import sys
import argparse
import logging
from . import Loader
from . import logger
from . import mongo_loader as ml
from . import rethink_loader as rl
from . import postgresql_loader as pg
from . import riak_loader as r
import os
import yaml

#
# Setup Logging
#


def setup_logs(logfile, verbose):
    ''' Setup general logging '''

    log = logging.FileHandler(logfile)
    console = logging.StreamHandler()
    logger.addHandler(console)
    logger.addHandler(log)
    logger.setLevel(logging.INFO)
    if verbose:
        logger.setLevel(logging.DEBUG)


def verify_file(filename):
    ''' Validate files '''

    logger.info('Validating %s' % filename)
    return os.path.isfile(filename)


def load_config(config):
    ''' Load configuration file '''

    if verify_file(config):
        try:
            with open(config, 'r') as conf:
                options = yaml.load(conf)

        except:
            logger.error('Unable to access config (%s)', e)
            return False
        return options
    return False


def main(dbtype, ldr, custom=None):
    ''' Main program '''

    logger.warning('Starting DB Load Tests')
    load_duration = []
    delete_duration = []
    if dbtype == 'mongo':
        logger.warning('Loading Mongo')
        logger.info('loading: %s:%d (%d)', ldr.host, ldr.port, ldr.concurrency)
    if dbtype == 'rethink':
        logger.warning('Loading Rethink')
        logger.info('loading: %s:%d (%d)', ldr.host, ldr.port, ldr.concurrency)
    if dbtype == 'postgres':
        logger.warning('Loading PostgreSQL')
        logger.info('loading: %s:%d (%d)', ldr.host, ldr.port, ldr.concurrency)
    if dbtype == 'riak':
        logger.warning('Loading Riak')
        logger.info('loading: %s:%d (%d)', ldr.host, ldr.port, ldr.concurrency)
    load_duration, delete_duration, update_duration, select_duration = ldr.load_run(custom)

    if not load_duration:
        logger.warning('0 load runs recorded')
    else:
        logger.warning('%d load runs in %4.3f seconds with avg run of %4.2f',
                       len(load_duration),
                       sum(load_duration),
                       len(load_duration) / sum(load_duration))
    if not delete_duration:
        logger.warning('0 delete runs recorded')
    else:
        logger.warning('%d delete runs in %4.3f seconds with avg run of %4.2f',
                       len(delete_duration),
                       sum(delete_duration),
                       len(delete_duration) / sum(delete_duration))
    if not update_duration:
        logger.warning('0 update runs recorded')
    else:
        logger.warning('%d update runs in %4.3f seconds with avg run of %4.2f',
                       len(update_duration),
                       sum(update_duration),
                       len(update_duration) / sum(update_duration))
    if not select_duration:
        logger.warning('0 select runs recorded')
    else:
        logger.warning('%d select runs in %4.3f seconds with avg run of %4.2f',
                       len(select_duration),
                       sum(select_duration),
                       len(select_duration) / sum(select_duration))
    logger.warning('Completed DB Load Tests')

if __name__ == "__main__":

    #
    # Parse command line options
    #

    parser = argparse.ArgumentParser(description='Check dbloader arguments')
    parser.add_argument('-c', '--config', default='./etc/load.yml',
                        help='Dbloader config (default=./etc/load.yml)')
    parser.add_argument('-l', '--log', default='./dbloader.log',
                        help='Dbloader Log (default=./dbloader.log)')
    parser.add_argument('-s', '--server', default='localhost',
                        help='Database Server / URL (default=localhost)')
    parser.add_argument('-t', '--type', default='mongo',
                        choices=['mongo', 'mysql', 'rethink', 'riak'],
                        help='Database Type [mongo|mysql|rethink|riak] (default=mongo)')
    parser.add_argument('-P', '--port', default=3306,
                        help='Database port (default=3306/27017/29015/8098)')
    parser.add_argument('-u', '--user',
                        help='Database user if necessary')
    parser.add_argument('-p', '--passwd',
                        help='Database password if necessary')
    parser.add_argument('--protocol', default='http',
                        help='Riak Protocol [http|protobuf] (default=http)')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='Debug Mode')
    args = parser.parse_args()

    setup_logs(args.log, args.verbose)
    logger.warning('Starting DB Load Tests')
    args.inserts = 250
    args.deletes = 250
    args.updates = 250
    args.selects = 250
    if args.config:
        options = load_config(args.config)
        if options:
            logger.info('Loaded: %s', options)
            args.server = options['server'][0]['name']
            args.type = options['server'][0]['type']
            args.port = options['server'][0]['port']
            args.user = options['server'][0]['user']
            args.concurrency = options['server'][0]['concurrency']
            args.passwd = options['server'][0]['pass']
            if options['server'][0]['protocol']:
                args.protocol = options['server'][0]['protocol']
            if options['server'][0]['inserts']:
                args.inserts = options['server'][0]['inserts']
            if options['server'][0]['deletes']:
                args.deletes = options['server'][0]['deletes']
            if options['server'][0]['updates']:
                args.updates= options['server'][0]['updates']
            if options['server'][0]['selects']:
                args.selects= options['server'][0]['selects']
        else:
            logger.error('Unable to load config file')
    else:
        logger.warning('Config file %s not found, using defaults',
                       args.config)

    if args.type == 'mongo':
        ldr = ml.rethinkLoader()
        ldr.concurrency = args.concurrency
        ldr.inserts = args.inserts
        ldr.inserts = args.deletes
        ldr.inserts = args.updates
        ldr.inserts = args.selects
        logger.info('loading: %s:%d (%d)', args.server, args.port, args.concurrency)
        load_duration, delete_duration, update_duration, select_duration = ldr.load_run()
    if args.type == 'rethink':
        ldr = rl.rethinkLoader()
        ldr.concurrency = args.concurrency
        ldr.inserts = args.inserts
        ldr.inserts = args.deletes
        ldr.inserts = args.updates
        ldr.inserts = args.selects
        logger.info('loading: %s:%d (%d)', args.server, args.port, args.concurrency)
        load_duration, delete_duration, update_duration, select_duration = ldr.load_run()
    if args.type == 'postgres':
        ldr = pg.PostgresLoader(args.server, args.port, args.user, args.passwd, 'postgres')
        ldr.concurrency = args.concurrency
        ldr.inserts = args.inserts
        ldr.inserts = args.deletes
        ldr.inserts = args.updates
        ldr.inserts = args.selects
        logger.info('loading: %s:%d (%d)', args.server, args.port, args.concurrency)
        load_duration, delete_duration, update_duration, select_duration = ldr.load_run()
    if args.type == 'riak':
        ldr = r.RiakLoader(args.protocol, args.server, args.port)
        ldr.concurrency = args.concurrency
        ldr.inserts = args.inserts
        ldr.inserts = args.deletes
        ldr.inserts = args.updates
        ldr.inserts = args.selects
        logger.info('loading: %s:%d (%d)', args.server, args.port, args.concurrency)
        load_duration, delete_duration, update_duration, select_duration = ldr.load_run()
    logger.warning('%d load runs in %4.2f time with avg run of %4.2f',
                   len(load_duration),
                   sum(load_duration),
                   len(load_duration) / sum(load_duration))
    logger.warning('%d delete runs in %4.2f time with avg run of %4.2f',
                   len(delete_duration),
                   sum(delete_duration),
                   len(delete_duration) / sum(delete_duration))
    logger.warning('Completed DB Load Tests')
