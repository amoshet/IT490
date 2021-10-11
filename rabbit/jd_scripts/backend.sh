x=$(systemctl show -p ActiveState --value apache2)
if [[ $x != *"inactive"* ]]
then
  echo "Back End is already running"
else
  echo "Starting up Back End"
  sudo service apache2 start
fi
exit
