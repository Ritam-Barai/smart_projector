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

# Run the main script
chmod +x . slideshow_script.sh
chmod +x . setup.sh

