#!/bin/bash

:<<COMMENT
#######################################
 
 After the initial bootup of the Raspberry Pi, the following steps are executed:

 Connect to a Wifi network and update the system

Run the following command to update the system:
 git clone "https://github.com/Ritam-Barai/smart_projector.git"

then run this script:
bash ~/smart_projector/setup.sh

Recommended: sudo date MMDDhhmmYYYY to set the correct date and time
Can cause SSL errors if not set correctly


Note: After imaging, dtoverlap=,,, has some problem. Comment it before mounting it on RPi
Run rpi-update then unmount and  uncomment dtoverlay=,,, and mount it back on RPi
######################################
COMMENT



# Enable NTP synchronization
#sudo timedatectl set-ntp true

# Restart systemd-timesyncd service to ensure it syncs immediately
#sudo systemctl restart systemd-timesyncd.service

# Check the updated time
date


sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install --upgrade python3-pip
sudo apt install lsof xinit xorg python-xdg openbox python3-tk mupdf net-tools libmicrohttpd-dev -y


cd smart_projector || exit
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt


# Run the main script
chmod +x . slideshow_script.sh
chmod +x . setup.sh
chmod +x . server_script.sh
chmod +x . hotspot.sh

