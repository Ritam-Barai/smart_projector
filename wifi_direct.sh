#!/bin/bash

# Step 1: Enable Wi-Fi Direct (P2P Wi-Fi) on Raspberry Pi
echo "Starting Wi-Fi Direct (P2P Wi-Fi) interface..."
sudo iw dev wlan0 interface add p2p-dev-wlan0 type managed
sudo ip link set dev p2p-dev-wlan0 up
echo "Wi-Fi Direct (P2P Wi-Fi) interface started."

# Step 2: Connect a Device via Wi-Fi Direct
echo "Please connect your device via Wi-Fi Direct (P2P Wi-Fi)."

# Step 3: Assign a Private IP Address to the Connected Device
echo "Assigning IP address 10.11.0.69/24 to the connected device..."
sudo ip addr add 10.11.0.69/24 dev p2p-dev-wlan0
echo "IP address assigned to the connected device."

# Step 4: Configure Routing and NAT
echo "Enabling IP forwarding..."
sudo sysctl net.ipv4.ip_forward=1

echo "Configuring NAT (Network Address Translation)..."
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE

# Change the owner of the file to the current user
sudo chown $(whoami):$(whoami) /etc/iptables/rules.v4

# Allow the owner to read and write, and deny others (replace with appropriate permissions)
sudo chmod 600 /etc/iptables/rules.v4

echo "Saving iptables rules..."
sudo iptables-save > /etc/iptables/rules.v4

# Step 5: Test Connectivity
#echo "Testing connectivity from the connected device..."
# Optionally, you can add a ping test or other connectivity tests here

#echo "Setup complete. The connected device should now have internet access through your Raspberry Pi."
