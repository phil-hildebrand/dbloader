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
usage: dbloader.py [-h] [-c CONFIG] [-l LOG] [-s SERVER]
                   [-t {mongo,mysql,rethink}] [-P PORT] [-u USER] [-p PASSWD]
                   [-v]

Check dbloader arguments

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Dbloader config (default=./etc/load.yml)
  -l LOG, --log LOG     Dbloader Log (default=./dbloader.log)
  -s SERVER, --server SERVER
                        Database Server / URL (default=localhost)
  -t {mongo,mysql,rethink}, --type {mongo,mysql,rethink}
                        Database Type [mongo|mysql|rethink] (default=mongo)
  -P PORT, --port PORT  Database port (default=3306/27017/29015)
  -u USER, --user USER  Database user if necessary
  -p PASSWD, --passwd PASSWD
                        Database password if necessary
  -v, --verbose         Debug Mode
```
