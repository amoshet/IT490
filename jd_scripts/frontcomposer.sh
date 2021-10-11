#!/bin/bash

#Apache2
x=$(systemctl show -p ActiveState --value apache2)
if [[ $x != *"inactive"* ]]
then
  echo "Apache Web Server is already running"
else
  echo "Starting up Apache Web Server"
  sudo service apache2 start
fi
