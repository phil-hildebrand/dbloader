#!/usr/bin/env bash
cd /vagrant
apt-get update
apt-get install -y python-setuptools build-essential libssl-dev libffi-dev python-dev git
easy_install pip
pip install --upgrade virtualenv
virtualenv venv
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
. /etc/lsb-release; VERSION=$DISTRIB_CODENAME;echo "deb http://repo.mongodb.org/apt/ubuntu $VERSION/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
. /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y build-essential python-dev
sudo apt-get install -y python-pip
pip install -r /vagrant/requirements.txt
sudo apt-get install -y mongodb-org
sudo apt-get install -y postgresql
sudo apt-get update
sudo apt-get install rethinkdb
sudo apt-get install -y rethinkdb
sudo sed -i "s/^\(.*bindIp.*\)/# \1/" /etc/mongod.conf
sudo service mongod restart

. /vagrant/venv/bin/activate
pip install -r requirements.txt
echo ". /vagrant/venv/bin/activate" >> ~vagrant/.bashrc
