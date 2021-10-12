#!/bin/bash
#mysql
x=$(systemctl show -p ActiveState --value mysql)
if [[ $x != *"inactive"* ]]
then
  echo "Database is already running"
else
  echo "Starting up Database"
  sudo service mysql start
fi
#RabbitMQ
ssh -o ConnectTimeout=10 34.66.184.176 'bash -s' < ./rabbit.sh

#frontend Database
ssh -o ConnectTimeout=10 104.154.121.50 'bash -s' < ./front.sh

#backend
ssh -o ConnectTimeout=10 34.72.26.172 'bash -s' < ./backend.sh
