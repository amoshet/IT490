d=$(systemctl show -p ActiveState --value mysql)
if [[ $d != *"inactive"* ]]
then
  echo "MYSQL is already running"
else
  echo "Starting up MYSQL Database"
  sudo service mysql start
fi
exit
