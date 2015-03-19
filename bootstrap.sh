#!/usr/bin/env bash

# update packages
apt-get update

# install python dependencies
apt-get install -y python-pip
pip install django
pip install djangorestframework

# other useful tools
apt-get install -y curl

# install mysql server
apt-get install -y debconf-utils
echo 'mysql-server mysql-server/root_password password 1234' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password 1234' | debconf-set-selections
apt-get install -y mysql-server

# install phpmyadmin
apt-get install -y apache2
echo 'phpmyadmin phpmyadmin/dbconfig-install boolean true' | debconf-set-selections
echo 'phpmyadmin phpmyadmin/app-password-confirm password 1234' | debconf-set-selections
echo 'phpmyadmin phpmyadmin/mysql/admin-pass password 1234' | debconf-set-selections
echo 'phpmyadmin phpmyadmin/mysql/app-pass password 1234' | debconf-set-selections
echo 'phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2' | debconf-set-selections
apt-get install -y phpmyadmin
echo "Include phpmyadmin.conf" >> /etc/apache2/apache2.conf
ln -s /etc/phpmyadmin/apache.conf /etc/apache2/phpmyadmin.conf
php5enmod mcrypt
service apache2 restart
