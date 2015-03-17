#!/usr/bin/env bash

# update packages
apt-get update

# install python dependencies
apt-get install -y python-pip python-mysqldb
pip install iniparse sqlsoup flask hashids

# install mysql server
apt-get install -y debconf-utils
echo mysql-server mysql-server/root_password password 1234 | debconf-set-selections
echo mysql-server mysql-server/root_password_again password 1234 | debconf-set-selections
apt-get install -y mysql-server

# import database
mysql -u root -p1234 < /vagrant/db/database.sql
mysql -u root -p1234 < /vagrant/db/test-data.sql
