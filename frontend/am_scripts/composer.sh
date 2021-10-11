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
#RabbitMQ
ssh -o ConnectTimeout=10 34.66.184.176 'bash -s' < ./rabbit.sh

#MYSQL Database
ssh -o ConnectTimeout=10 104.198.163.100 'bash -s' < ./mysql.sh

#backend
ssh -o ConnectTimeout=10 34.72.26.172 'bash -s' < ./backend.sh
