#!/bin/bash

# require root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# remove old script files
rm -rf /var/inv/inv
# replace with new script files
cp -r server/inv /var/inv/inv
