#!/bin/bash

PIDS=$(lsof -ti:8000 )
:<<'COMMENT'
cleanup() {
    echo "Cleaning up before exit..."
    # Perform any cleanup here
    exit 0
}
COMMENT

# Trap SIGINT and SIGTERM signals and call the cleanup function
trap cleanup SIGINT SIGTERM
# Check if PID is not empty
for PID in $PIDS; do
    echo "PID: $PID"
    if [ ! -z "$PID" ] && ps -p $PID -o comm= | grep -iq python; then
    # Kill the process
    openbox --exit
    sleep 1
    kill -SIGTERM $PID
    #sudo systemctl restart dnsmasq
    echo "Server on port 8000 has been stopped."
    sleep 2
    #openbox --exit
    sudo systemctl restart lighttpd
    sudo systemctl restart nodogsplash
    sudo systemctl restart hostapd
    sudo systemctl restart dnsmasq
    sleep 3
    reboot
    else
    echo "No python process is running on port 8000."
    fi
done  
