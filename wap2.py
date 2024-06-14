import os
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(1)
    return result.stdout

def setup_access_point(ssid, wpa_passphrase):
    # Update and install packages
    run_command("sudo apt update && sudo apt upgrade -y")
    run_command("sudo apt install hostapd dnsmasq -y")

    # Stop and disable services temporarily
    run_command("sudo systemctl stop hostapd")
    run_command("sudo systemctl stop dnsmasq")
    run_command("sudo systemctl disable hostapd")
    run_command("sudo systemctl disable dnsmasq")

    # Configure dnsmasq
    run_command("sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig")
    with open("/etc/dnsmasq.conf", "w") as file:
        file.write("interface=wlan0\n")
        file.write("dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h\n")

    # Configure static IP for wlan0
    with open("/etc/dhcpcd.conf", "a") as file:
        file.write("interface wlan0\n")
        file.write("static ip_address=192.168.4.1/24\n")
        file.write("nohook wpa_supplicant\n")

    # Configure hostapd
    with open("/etc/hostapd/hostapd.conf", "w") as file:
        file.write("interface=wlan0\n")
        file.write("driver=nl80211\n")
        file.write(f"ssid={ssid}\n")
        file.write("hw_mode=g\n")
        file.write("channel=7\n")
        file.write("wmm_enabled=0\n")
        file.write("macaddr_acl=0\n")
        file.write("auth_algs=1\n")
        file.write("ignore_broadcast_ssid=0\n")
        file.write("wpa=2\n")
        file.write(f"wpa_passphrase={wpa_passphrase}\n")
        file.write("wpa_key_mgmt=WPA-PSK\n")
        file.write("wpa_pairwise=TKIP\n")
        file.write("rsn_pairwise=CCMP\n")

    with open("/etc/default/hostapd", "a") as file:
        file.write("DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"\n")

    # Enable IP forwarding
    with open("/etc/sysctl.conf", "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(content.replace("#net.ipv4.ip_forward=1", "net.ipv4.ip_forward=1"))
        file.truncate()

    # Configure NAT with iptables
    run_command("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    run_command("sudo sh -c \"iptables-save > /etc/iptables.ipv4.nat\"")

    with open("/etc/rc.local", "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(content.replace("exit 0", "iptables-restore < /etc/iptables.ipv4.nat\nexit 0"))
        file.truncate()

    # Restart services and enable on boot
    run_command("sudo systemctl unmask hostapd")
    run_command("sudo systemctl enable hostapd")
    run_command("sudo systemctl enable dnsmasq")
    run_command("sudo systemctl start hostapd")
    run_command("sudo systemctl start dnsmasq")

if __name__ == "__main__":
    ssid = "YourNetworkName"
    wpa_passphrase = "YourPassphrase"
    setup_access_point(ssid, wpa_passphrase)
