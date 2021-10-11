d=$(systemctl show -p ActiveState --value mysql)
if [[ $d != *"inactive"* ]]
then
  echo "Database is already running"
else
  echo "Starting up Database"
  sudo service mysql start
fi
exit
