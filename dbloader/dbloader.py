#!/usr/bin/python

import sys
import argparse
import logging
import mongo.mongo_loader as ml
import random
import string
import os
import yaml

#
# Setup Logging
#


def setup_logs(logfile, verbose):
    ''' Setup general logging '''

    global logger
    logger = logging.getLogger('dbloader')

    log = logging.FileHandler(logfile)
    console = logging.StreamHandler()

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(log)
    else:
        logger.setLevel(logging.WARNING)
        logger.addHandler(log)


def verify_file(filename):
    ''' Validate files '''

    logger.info('Validating %s' % filename)
    return(os.path.isfile(filename))


def load_config(config):
    ''' Load configuration file '''

    if verify_file(config):
        try:
            with open(config, 'r') as conf:
                options = yaml.load(conf)

        except:
            logger.error('Unable to access config (%s)', e)
            return(False)
        return(options)
    return(False)


def main():
    ''' Main program '''

    logger.warning('Starting DB Load Tests')
    load_duration = []
    delete_duration = []
    load_duration, delete_duration = ml.load_run()
    logger.warning('%d load runs in %4.2f time with avg run of %4.2f',
                   len(load_duration),
                   sum(load_duration),
                   len(load_duration) / sum(load_duration))
    logger.warning('%d delete runs in %4.2f time with avg run of %4.2f',
                   len(delete_duration),
                   sum(delete_duration),
                   len(delete_duration) / sum(delete_duration))
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
                        choices=['mongo', 'mysql'],
                        help='Database Type [mongo|mysql] (default=mongo)')
    parser.add_argument('-P', '--port', default=3306,
                        help='Database port (default=3306/27017/29015)')
    parser.add_argument('-u', '--user',
                        help='Database user if necessary')
    parser.add_argument('-p', '--passwd',
                        help='Database password if necessary')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='Debug Mode')
    args = parser.parse_args()

    setup_logs(args.log, args.verbose)
    logger.warning('Starting DB Load Tests')
    if (args.config):
        options = load_config(args.config)
        if options:
            logger.info('Loaded: %s', options)
            args.server = options['server'][0]['name']
            args.type = options['server'][0]['type']
            args.port = options['server'][0]['port']
            args.user = options['server'][0]['user']
            args.concurrency = options['server'][0]['concurrency']
            args.passwd = options['server'][0]['pass']
            if options['server'][0]['inserts']:
                ml.inserts = options['server'][0]['inserts']
            if options['server'][0]['deletes']:
                ml.deletes = options['server'][0]['deletes']
        else:
            logger.error('Unable to load config file')
    else:
        logger.warning('Config file %s not found, using defaults',
                       args.config)
        ml.inserts = 250
        ml.deletes = 250

    ml.host = args.server
    ml.port = args.port
    ml.concurrency = args.concurrency
    ml.load_run()
    logger.warning('%d load runs in %4.2f time with avg run of %4.2f',
                   len(load_duration),
                   sum(load_duration),
                   len(load_duration) / sum(load_duration))
    logger.warning('%d delete runs in %4.2f time with avg run of %4.2f',
                   len(delete_duration),
                   sum(delete_duration),
                   len(delete_duration) / sum(delete_duration))
    logger.warning('Completed DB Load Tests')
