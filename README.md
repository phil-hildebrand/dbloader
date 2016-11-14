# Overview

Basic load test tool for databases

![](https://travis-ci.org/phil-hildebrand/dbloader.svg?branch=master)

# Requirements

- python 2.7
- pip

# Installation

- Clone https://github.com/phil-hildebrand/dbloader locally


```
$ python setup.py install
```

## Dev Environment Setup

- Assumes Virtualbox Installed
- Vagrant >= 1.7.2

```
  $ cd <repo_path>/dbloader
  $ vagrant box add ubuntu/trusty64
  $ vagrant up
```

## _Usage_

```
usage: dbloader.py [-h] [-c CONFIG] [-l LOG] [-s SERVER] [-t {mongo,mysql}]
                   [-P PORT] [-u USER] [-p PASSWD] [-v]

Check dbloader arguments

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Dbloader config file (default = ./etc/load.yml)
  -l LOG, --log LOG     Dbloader Log file (default = ./dbloader.log)
  -s SERVER, --server SERVER
                        Database Server / URL (default = localhost)
  -t {mongo,mysql}, --type {mongo,mysql}
                        Database Server Type [mongo|mysql] (default = mongo)
  -P PORT, --port PORT  Database port (defaults to 3306 for MySQL, 27017 for
                        mongo)
  -u USER, --user USER  Database user if necessary
  -p PASSWD, --passwd PASSWD
                        Database password if necessary
  -v, --verbose         Debug Mode
```
