#!/usr/bin/env bash
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
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y mongodb-org
# sudo apt-get install -y postgresql
sudo apt-get install -y rethinkdb
sudo sed "s/^#\(.*bind.*\)/bind=all/" /etc/rethinkdb/default.conf.sample > /etc/rethinkdb/instances.d/instance1.conf
sudo sed -i "s/^\(.*bindIp.*\)/# \1/" /etc/mongod.conf
sudo service mongod restart
. /vagrant/p3env/bin/activate
cd /vagrant
pip install -r requirements.txt
python setup.py install
pytest -v tests
. /vagrant/venv/bin/activate
python setup.py install
pytest -v tests
pip install -r requirements.txt
echo ". /vagrant/p3env/bin/activate; cd /vagrant" >> ~vagrant/.bashrc
