#!/bin/bash


export PATH=$PATH:$HOME/smart_projector/server_proj/projview
FILE_PATH=$HOME/smart_projector/server_proj/projview
#echo "$PATH"

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

source smart_projector/env/bin/activate
cd "$FILE_PATH" || exit



python3 manage.py runserver "$IP_ADDR:8000"
