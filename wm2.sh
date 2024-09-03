#!/bin/bash


#export PATH=$PATH:/home/pi/smart_projector/server_proj/projview
#export XAUTHORITY=/home/pi/.Xauthority
#startx -- -nocursor
#sleep 3

###!/bin/bash

# Replace 'wlan0' with your actual Wi-Fi interface name
INTERFACE='wlan0'

# Function to check if the interface is up
is_interface_up() {
    ip link show "$INTERFACE" | grep -q 'state UP'
}

# Function to check if the interface is operating as a hotspot
is_hotspot_active() {
    # Check if the Wi-Fi interface has an IP address
    ip addr show "$INTERFACE" | grep -q 'inet '
    # Check for hotspot mode (assuming hostapd is being used for hotspot)
    # You may need to adapt this based on how your hotspot is configured
    hostapd_cli status | grep -q 'ap_isolate=1'
}

# Wait for the interface to be up and hotspot to be active
while true; do
    if is_interface_up && is_hotspot_active; then
        echo "Wi-Fi interface is active and operating as a hotspot. Starting startx..."
        startx -- -nocursor
        sleep 1
        break
    else
        echo "Waiting for Wi-Fi interface to be active and operating as a hotspot..."
        sleep 10  # Wait for 10 seconds before checking again
    fi
done