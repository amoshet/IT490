#!/user/bin/sh
r=$(systemctl show -p ActiveState --value rabbitmq-server)
if [[ $r != *"inactive"* ]]
then
  echo "RabbitMQ is already running"
else
  echo "Starting up RabbitMQ Server"
  sudo service rabbitmq-server start
fi

#Front-End
ssh 34.66.184.176 'bash -s' < ./frontcomposer.sh
#MYSQL Database
ssh 104.198.163.100 'bash -s' < ./mysql.sh
exit
#backend
#TO BE ADDED
