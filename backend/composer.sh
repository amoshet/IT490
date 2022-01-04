#!/bin/bash
#Apache2
x=$(systemctl show -p ActiveState --value apache2)
if [[ $x != *"inactive"* ]]
then
  echo "Back End is already running"
else
  echo "Starting up Back End"
  sudo service apache2 start
fi
#RabbitMQ
ssh -o ConnectTimeout=10 34.66.184.176 'bash -s' < ./rabbit.sh

#MYSQL Database
ssh -o ConnectTimeout=10 104.198.163.100 'bash -s' < ./mysql.sh

#backend
ssh -o ConnectTimeout=10 104.154.121.50 'bash -s' < ./frontcomposer.sh
