#!/bin/bash

# require root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# install necessary 3rd party pkg
echo "inv: updating Ubuntu"
apt-get update &>/dev/null
echo "inv: installing pkgs"
read -s -p "Enter a password: " pw
echo -e "$pw\n$pw" | apt-get install apache2 libapache2-mod-wsgi mysql-server python-dev python-pip -y &>/dev/null
echo "inv: installing python pkgs"
pip install -r requirements.txt &>/dev/null

# setup mysql
echo "inv: initializing database"
echo -e "$pw\n" | mysql -u root -p -e "create database inv"; 

# setup dir
echo "inv: setting up inv directory"
ln -s `pwd`/server /var/www/inv

# setup ssl
echo "inv: setting up ssl"
a2enmod ssl &>/dev/null
mkdir /etc/apache2/ssl 
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt

# setup apache
echo "inv: setting up apache"
cp conf/inv.conf /etc/apache2/sites-available
a2ensite inv &>/dev/null
service apache2 reload
