#!/usr/bin/env bash
# postgres version
PG_VERSION=10
cd /vagrant
apt-get update
apt-get install -y python-setuptools build-essential libssl-dev libffi-dev python-dev git
easy_install pip
pip install --upgrade virtualenv
virtualenv venv
virtualenv -p python3 p3env
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
. /etc/lsb-release; VERSION=$DISTRIB_CODENAME;echo "deb http://repo.mongodb.org/apt/ubuntu $VERSION/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
. /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
. /etc/lsb-release && echo "deb http://apt.postgresql.org/pub/repos/apt/ $DISTRIB_CODENAME-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
sudo apt-get update
sudo apt-get install -y mongodb-org
# sudo apt-get install -y postgresql
sudo apt-get install -y rethinkdb
sudo apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"
sudo sed "s/^#\(.*bind.*\)/bind=all/" /etc/rethinkdb/default.conf.sample > /etc/rethinkdb/instances.d/instance1.conf
sudo sed -i "s/^\(.*bindIp.*\)/# \1/" /etc/mongod.conf
# postgres configs
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"
# Edit postgresql.conf to change listen address to '*':
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"
sudo service postgresql restart
sudo service mongod restart
sudo service rethinkdb restart

# initial role setup for postgres
cat << EOF | su - postgres -c psql
CREATE ROLE DBA WITH SUPERUSER LOGIN PASSWORD 'dba';
EOF

. /vagrant/p3env/bin/activate
cd /vagrant
pip install -r requirements.txt
python setup.py install
pytest -v tests
sudo service rethinkdb status
. /vagrant/venv/bin/activate
pip install -r requirements.txt
python setup.py install
pytest -v tests
echo ". /vagrant/p3env/bin/activate; cd /vagrant" >> ~vagrant/.bashrc

