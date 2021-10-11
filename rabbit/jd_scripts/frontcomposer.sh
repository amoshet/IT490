#!/bin/bash

#Apache2
x=$(systemctl show -p ActiveState --value apache2)
if [[ $x != *"inactive"* ]]
then
  echo "Front End is already running"
else
  echo "Starting up Front End"
  sudo service apache2 start
fi
