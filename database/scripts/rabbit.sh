r=$(systemctl show -p ActiveState --value rabbitmq-server)
if [[ $r != *"inactive"* ]]
then
  echo "RabbitMQ is already running"
else
  echo "Starting up RabbitMQ Server"
  sudo service rabbitmq-server start
fi
exit
