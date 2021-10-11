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
ssh -o ConnectTimeout=10 34.66.184.176 'bash -s' < ./frontcomposer.sh
#MYSQL Database
ssh -o ConnectTimeout=10 104.198.163.100 'bash -s' < ./mysql.sh
#Backend
ssh -o ConnectTimeout=10 34.72.26.172 'bash -s' < ./backend.sh
exit
#backend
#TO BE ADDED
