#!/bin/bash

# Recreate the /etc/resolv.conf file
sudo touch /etc/resolv.conf

# Add Google's public DNS servers to the file
echo -e "nameserver 8.8.8.8\nnameserver 8.8.4.4" | sudo tee /etc/resolv.conf

# Ensure the file is not overwritten
sudo chattr +i /etc/resolv.conf

echo "/etc/resolv.conf has been recreated and configured."
