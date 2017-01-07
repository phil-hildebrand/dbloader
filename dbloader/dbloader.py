#!/usr/bin/python

import argparse
import logging
import mongo_loader
import random
import string
import os
import yaml

#
# Setup Logging
#

def setup_logs(logfile, verbose):
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

#
# Validate file(s)
#
def verify_file(filename):
    logger.info('Validating %s' % filename)
    return(os.path.isfile(filename))

def load_config(config):
    if verify_file(config):
        try:
            with open (config, 'r') as conf:
                options = yaml.load(conf)

        except:
             logger.error('Unable to access config (%s)', e)
             return(False)
        return(options)
    return(False)

def main():
    logger.warning('Starting DB Load Tests')
    mongo_loader.load_run()

if __name__ == "__main__":

    #
    # Parse command line options
    #

    parser = argparse.ArgumentParser(description='Check dbloader arguments')
    parser.add_argument('-c', '--config', default='./etc/load.yml',
                        help = 'Dbloader config file (default = ./etc/load.yml)')
    parser.add_argument('-l', '--log', default='./dbloader.log',
                        help = 'Dbloader Log file (default = ./dbloader.log)')
    parser.add_argument('-s', '--server', default='localhost',
                        help = 'Database Server / URL (default = localhost)')
    parser.add_argument('-t', '--type', default='mongo', choices=['mongo', 'mysql'],
                        help = 'Database Server Type [mongo|mysql] (default = mongo)')
    parser.add_argument('-P', '--port', default=3306, help = 'Database port (defaults to 3306 for MySQL, 27017 for mongo)')
    parser.add_argument('-u', '--user', help = 'Database user if necessary')
    parser.add_argument('-p', '--passwd', help = 'Database password if necessary')
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Debug Mode')
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
            args.passwd = options['server'][0]['pass']
            mongo_loader.inserts = options['server'][0]['inserts']
            mongo_loader.deletes = options['server'][0]['deletes']
        else:
            logger.error('Unable to load config file')
            mongo_loader.inserts = 250
            mongo_loader.deletes = 250
    else:
        logger.warning('Config file %s not found, using command line options' % args.config)

    mongo_loader.host = args.server
    mongo_loader.port = args.port
    mongo_loader.concurrency = 10
    mongo_loader.load_run()
