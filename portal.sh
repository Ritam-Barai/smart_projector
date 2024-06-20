sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.69.69.69:8000
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o wlan0 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4

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

sudo systemctl restart udhcpd

sudo systemctl enable monitor_dhcp.service
sudo systemctl start monitor_dhcp.service