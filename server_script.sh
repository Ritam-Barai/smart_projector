#!/bin/bash


export PATH=$PATH:/home/pi/smart_projector/server_proj/projview
FILE_PATH=/home/pi/smart_projector/server_proj/projview
#echo "$PATH"
#DJANGO_URL="http://10.69.69.1:8000"

# Function to get IP address using ip command
get_ip_with_ip() {
  ip addr show  | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | sed -n '2p'
}

# Function to get IP address using ifconfig command
get_ip_with_ifconfig() {
  ifconfig wlan0 | grep 'inet ' | awk '{print $2}'
}

# Determine which command to use for getting the IP address
if command -v ip &>/dev/null; then
  echo "$PWD"
  IP_ADDR=$(get_ip_with_ip)
elif command -v ifconfig &>/dev/null; then
  IP_ADDR=$(get_ip_with_ifconfig)
else
  echo "Neither 'ip' nor 'ifconfig' command is available."
  exit 1
fi

# Check if an IP address was found
if [ -z "$IP_ADDR" ]; then
  echo "No IP address found for Wi-Fi interface."
  exit 1
fi

# Path to the settings.py file
SETTINGS_FILE="$FILE_PATH/projview/settings.py"

# Update the HOST_IP variable in settings.py
sed -i "s/^HOST_IP = .*/HOST_IP = '$IP_ADDR'/" $SETTINGS_FILE

echo "Updated HOST_IP to $IP_ADDR in $SETTINGS_FILE"

VENV_PATH="/home/pi/smart_projector/env/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "Activating the virtual environment..."
    source "$VENV_PATH"
else
    echo "Virtual environment not found. Skipping activation."
fi
cd "$FILE_PATH" || exit
DJANGO_URL="http://$IP_ADDR:8000"


python3 manage.py runserver "$IP_ADDR:8000" &
sleep 1
echo "Starting server!"
:<<COMMENT
export XAUTHORITY=/home/pi/.Xauthority
while true;do
  if curl --output /dev/null --silent --head --fail "$DJANGO_URL";then
    #startx -- -nocursor
    startx
    sleep 1
    break
  else
    sleep 1
  fi
done 
#sudo systemctl stop hostapd
#sudo truncate -s 0 /var/lib/misc/udhcpd.leases
COMMENT
#sleep 1

#openbox --exit
#reboot
#sudo systemctl start hostapd
sudo systemctl restart lighttpd
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq
