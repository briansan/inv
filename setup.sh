#!/bin/sh

# require root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# install necessary 3rd party pkg
apt-get update
apt-get install apache2 libapache2-mod-wsgi mysql-server python-dev python-pip
pip install -r requirements.txt

# setup mysql
mysql -u root -p -e "create database inv"; 

# setup dir
cp -r server /var/www/inv

# setup apache
a2enmod ssl
cp conf/inv.conf /etc/apache2/sites-available
a2ensite inv
service apache2 reload
