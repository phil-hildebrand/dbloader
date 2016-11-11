#!/usr/bin/python

import argparse
import logging
import random
import string
import os

#
# Parse command line options
#

parser = argparse.ArgumentParser(description='Check dbloader arguments')
parser.add_argument('-l', '--log', default='/var/log/dbloader.log',
                    help = 'Dbloader Log file (default = /var/log/dbloader.log)')
parser.add_argument('-s', '--server', default='localhost',
                    help = 'Database Server / URL (default = localhost)')
parser.add_argument('-t', '--type', default='mongo', choices=['mongo', 'mysql'],
                    help = 'Database Server Type [mongo|mysql] (default = mongo)')
parser.add_argument('-P', '--port', default=3306,
                    help = 'Database port (defaults to 3306 for MySQL, 27017 for mongo)')
parser.add_argument('-u', '--user', help = 'Database user if necessary')
parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Debug Mode')
args = parser.parse_args()

#
# Setup Logging
#

logger = logging.getLogger('dbloader')

log = logging.FileHandler(args.log)
console = logging.StreamHandler()


if args.verbose:
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.addHandler(log)
else:
    logger.setLevel(logging.WARNING)
    logger.addHandler(log)


logger.warning('Starting DB Load Tests')
