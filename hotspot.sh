#!/bin/bash
sudo apt install hostapd udhcpd -y
 
sudo cat << EOF >/etc/udhcpd.conf
start 10.69.69.69 # This is the range of IPs that the hostspot will give to client devices.
end 10.69.69.69
interface wlan0 # The device uDHCP listens on.
remaining yes
opt dns 8.8.8.8 8.8.4.4 # The DNS servers client devices will use.
opt subnet 255.255.255.0
opt router 10.69.69.1 # The Pi's IP address on wlan0 which we will set up shortly.
opt lease 864000 # 10 day DHCP lease time in seconds
EOF
 
sudo echo 'DHCPD_OPTS="-S"' > /etc/default/udhcpd
 
ifconfig wlan0 10.69.69.1/24
 
sudo cat << EOF >/etc/hostapd/hostapd.conf
interface=wlan0
ssid=PRO_jector
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
EOF
 
sudo cat << EOF >/etc/network/interfaces
auto lo
 
iface lo inet loopback
#iface eth0 inet dhcp
 
#allow-hotplug wlan0
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp
 
iface wlan0 inet static
  address 10.69.69.1
  netmask 255.255.255.0
 
#up iptables-restore < /etc/iptables.ipv4.nat
EOF
 
sudo echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' > /etc/default/hostapd
 
#sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
#echo 'net.ipv4.ip_forward=1' > /etc/sysctl.conf
#iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
#iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
#iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
 
#sh -c "iptables-save > /etc/iptables.ipv4.nat"
 
#service hostapd start
#service udhcpd start
#sudo systemctl start udhcpd
#sudo systemctl enable hostapd
#sudo systemctl enable udhcpd
 
#update-rc.d hostapd enable
#update-rc.d udhcpd enable

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.69.69.69:8000
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o wlan0 -j ACCEPT
sudo iptables-save > /etc/iptables.rules.v4

sudo cat << EOF >/etc/systemd/system/start_django_and_monitor.sh
#!/bin/bash

LEASES_FILE="/var/lib/misc/dnsmasq.leases"
DJANGO_DIR="~/smart_projector/server_proj/projview"
DJANGO_PORT=8000
DJANGO_MANAGE="$DJANGO_DIR/manage.py"
CAPTIVE_PORTAL_URL="http://10.69.69.69:$DJANGO_PORT"

# Get the display port from the argument
DISPLAY_PORT=$1

if [ -z "$DISPLAY_PORT" ]; then
    echo "Usage: $0 <display_port>"
    exit 1
fi

# Function to launch the browser
launch_browser() {
    URL=$1
    if command -v chromium-browser &> /dev/null; then
        sudo -u pi DISPLAY=:${DISPLAY_PORT} chromium-browser $URL &
    elif command -v firefox &> /dev/null; then
        sudo -u pi DISPLAY=:${DISPLAY_PORT} firefox $URL &
    elif command -v safari &> /dev/null; then
        sudo -u pi DISPLAY=:${DISPLAY_PORT} safari $URL &
    else
        echo "No supported browser found."
    fi
}

# Start Django server
cd $DJANGO_DIR
python3 $DJANGO_MANAGE runserver 0.0.0.0:$DJANGO_PORT &

while true; do
    inotifywait -e modify $LEASES_FILE
    sleep 1
    if [ -f $LEASES_FILE ]; then
        IP_ADDRESS=$(tail -n 1 $LEASES_FILE | awk '{print $3}')
        echo "Launching browser for IP: $IP_ADDRESS"
        #launch_browser $CAPTIVE_PORTAL_URL
    fi
done


 
EOF

sudo chmod +x /usr/local/bin/start_django_and_monitor.sh


sudo cat << EOF >/etc/systemd/system/monitor_dhcp.service
[Unit]
Description=Monitor DHCP Leases and Launch Browser
After=network.target

[Service]
ExecStart=/usr/local/bin/start_django_and_monitor.sh 0
Restart=always
User=root

[Install]
WantedBy=multi-user.target

 
EOF

service hostapd start
service udhcpd start
sudo systemctl start udhcpd
sudo systemctl enable hostapd
sudo systemctl enable udhcpd
 
update-rc.d hostapd enable
update-rc.d udhcpd enable
sudo systemctl restart udhcpd

sudo systemctl enable monitor_dhcp.service
sudo systemctl start monitor_dhcp.service
