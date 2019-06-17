# Overview

Basic load test tool for databases

## Supported Databases
- MongoDB
- RethinkDB
- PostgreSQL
- Riak

![](https://travis-ci.org/phil-hildebrand/dbloader.svg?branch=master)

# Requirements

- python 3 ( With Riak loader, use 3.6 )
- pip

# Installation

- Clone https://github.com/phil-hildebrand/dbloader locally
- Navigate to dbloader/
- Install / Update dependancies with `pip install -r requirements.txt`.
_Note: if using virtual environments for python, setup your virtual environment before running pip_
- Install the dbloader:
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

# Configuration

Dbloader can be configured to perform concurrent inserts, selects, deletes and updates. The settings can be updated in a config file which can then be passed as input to the loader.
Sample yaml config:

```
server:
- name: servername
  type: rethink
  port: 28015
  user: none
  pass: none
  concurrency: 24
  inserts: 50
  selects: 50
  deletes: 25
  updates: 25
```
## Custom data loading

Dbloader can also be configured to load custom data into the database. For providing custom inputs update the config file to include a paramater named **custom** and specify the operation to be performed.
_Please refer to etc/load.yml for sample custom configs._

### Custom options
- ctype [insert | select | delete | update]: Type of crud operation.
- database: Database/Bucket name for the crud operation. A new db will be created if it doesn't exist.
- table: Table/Collection name where the crud is to be performed. A new table/collection will be created if it doesn't exist.
- table_create_script: Description of table with column names, size and types. Will be used to create new table if table does not exist. Required in case of sql databases.
- limit: Number of records to be fetched/updated/deleted.
- column/ columntype: Name and type of column to be updated. Required in sql databases for update operations.
- insert: data to be inserted into the table. Required in case of insert operations. Data should be given in json format. For sql databases `columnname: columnvalue` format should be used.
- update: Value to be updated.

## Examples

Please refer to examples directory for sample usage for different databases.
