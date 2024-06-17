#!/bin/bash

:<<COMMENT
#######################################
 
 After the initial bootup of the Raspberry Pi, the following steps are executed:

 Connect to a Wifi network and update the system

Run the following command to update the system:
 git clone "https://github.com/Ritam-Barai/smart_projector.git"

then run this script:
bash ~/smart_projector/setup.sh


######################################
COMMENT



# Enable NTP synchronization
sudo timedatectl set-ntp true

# Restart systemd-timesyncd service to ensure it syncs immediately
sudo systemctl restart systemd-timesyncd.service

# Check the updated time
date



cd smart_projector || exit
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

# Variables
INTERFACE="wlan0"
SSID="PROjector"

IP_ADDRESS="10.11.0.1/24"
DHCP_START="10.11.0.69"
DHCP_END="10.11.0.69"

# Create hotspot
nmcli dev wifi hotspot ifname $INTERFACE ssid $SSID password $PASSWORD

# Configure DHCP range
nmcli connection modify $SSID ipv4.addresses $IP_ADDRESS
nmcli connection modify $SSID ipv4.method shared
nmcli connection modify $SSID ipv4.dhcp-start $DHCP_START
nmcli connection modify $SSID ipv4.dhcp-end $DHCP_END

# Run the main script
chmod +x . slideshow_script.sh
chmod +x . setup.sh

