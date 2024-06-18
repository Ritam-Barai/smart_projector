#!/bin/bash

# Variables
INTERFACE="wlan0"
SSID="PROjector"
HOTSPOT_ADDRESS="10.11.0.1/24"
IP_ADDRESS="10.11.0.69"

sudo apt-get upgrade NetworkManager

# Create hotspot without password
nmcli dev wifi hotspot ifname $INTERFACE ssid $SSID
nmcli connection modify Hotspot connection,id $SSID
nmcli connection modify $SSID ipv4.addresses $HOTSPOT_ADDRESS
nmcli connection modify $SSID ipv4.method shared

nmcli connection down $SSID


sudo apt install dnsmasq
sudo service dnsmasq stop

sudo cat <<EOF > /etc/dnsmasq.conf
interface=$INTERFACE
dhcp-range=$IP_ADDRESS,$IP_ADDRESS,255.255.255.0,24h
EOF

sudo service dnsmasq start
nmcli connection up $SSID

reboot

<<COMMENT
# Create custom DNSMasq configuration
sudo mkdir -p /etc/NetworkManager/dnsmasq-shared
echo "dhcp-range=$IP_ADDRESS,$IP_ADDRESS,12h" | sudo tee /etc/NetworkManager/dnsmasq-shared/$SSID.conf

# Configure NetworkManager to use custom DNSMasq configuration
echo -e "[connection]\nid=$SSID\n\n[ipv4]\nmethod=shared" | sudo tee /etc/NetworkManager/conf.d/$SSID.conf

# Restart NetworkManager
sudo systemctl restart NetworkManager

# Restart the hotspot connection
nmcli connection down $SSID
nmcli connection up $SSID

echo "Open hotspot configured with a single DHCP client limit"