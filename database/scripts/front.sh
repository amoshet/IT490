x=$(systemctl show -p ActiveState --value apache2)
if [[ $x != *"inactive"* ]]
then
  echo "Front end is already running"
else
  echo "Starting up Front end"
  sudo service apache2 start
fi
exit
