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
echo -e "$pw\n$pw" | apt-get install apache2 libapache2-mod-wsgi python-dev python-pip -y &>/dev/null

echo "inv: installing python pkgs"
pip install -r requirements.txt &>/dev/null

# setup dir
echo "inv: setting up inv directory"
cp -r `pwd`/server /var/inv
chown -R www-data /var/inv
chgrp -R www-data /var/inv

# setup ssl
echo "inv: setting up ssl"
a2enmod ssl &>/dev/null
mkdir /etc/apache2/ssl 
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt

# setup conf
echo "inv: setting up apache conf"
cp conf/inv.conf /etc/apache2/sites-available
echo "<Directory /var/inv/>
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>" >> /etc/apache2/apache2.conf
      

# setup apache
echo "inv: initializing apache"
a2ensite inv &>/dev/null
service apache2 reload
