import subprocess
import psutil
import time

AP_SSID = "TestAP"
AP_PASSPHRASE = "12345678"
WLAN_INTERFACE = "wlan0"
DHCP_RANGE = "192.168.4.2,192.168.4.2"
DHCP_SUBNET = "255.255.255.0"

def get_wireless_interface():
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    interfaces = result.stdout.splitlines()
    for line in interfaces:
        if "wl" in line or "wlan" in line:
            # Extract interface name
            interface = line.split(":")[1].strip()
            return interface
    return None

def setup_hostapd(ssid, passphrase, interface):
    hostapd_conf = f"""
    interface={interface}
    driver=nl80211
    ssid={ssid}
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase={passphrase}
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    """
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(hostapd_conf)
    
    subprocess.run(["sudo", "systemctl", "unmask", "hostapd"])
    subprocess.run(["sudo", "systemctl", "enable", "hostapd"])
    subprocess.run(["sudo", "systemctl", "start", "hostapd"])

def setup_dnsmasq(interface, dhcp_range, dhcp_subnet):
    dnsmasq_conf = f"""
    interface={interface}
    dhcp-range={dhcp_range},{dhcp_subnet},24h
    """
    with open("/etc/dnsmasq.conf", "w") as f:
        f.write(dnsmasq_conf)

    subprocess.run(["sudo", "systemctl", "restart", "dnsmasq"])

def configure_network(interface):
    #subprocess.run(["sudo", "ifconfig", interface, "192.168.4.1", "netmask", DHCP_SUBNET])
    # Bring the interface up
    
    
    # Assign the IP address
    subprocess.run(["sudo", "ip", "addr", "add", "192.168.4.1/24", "dev", interface])
    subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"])
    subprocess.run(["sudo", "systemctl", "stop", "systemd-resolved"])
    subprocess.run(["sudo", "systemctl", "disable", "systemd-resolved"])
    subprocess.run(["sudo", "rm", "/etc/resolv.conf"])
    
    with open("/etc/resolv.conf", "w") as f:
        f.write("nameserver 8.8.8.8\nnameserver 8.8.4.4\n")
    #subprocess.run(["echo", "nameserver 8.8.8.8", "|", "sudo", "tee", "/etc/resolv.conf"])

def monitor_connections(interface):
    connected_clients = set()
    while True:
        connections = psutil.net_connections(kind='inet')
        active_clients = set(conn.raddr.ip for conn in connections if conn.laddr.ip == '192.168.4.1' and conn.raddr)
        new_clients = active_clients - connected_clients
        disconnected_clients = connected_clients - active_clients
        
        if new_clients:
            if len(connected_clients) == 0:
                print(f"New client connected: {new_clients}")
            else:
                for client in new_clients:
                    print(f"Dropping new connection from {client}")
                    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", client, "-j", "DROP"])
        
        if disconnected_clients:
            for client in disconnected_clients:
                print(f"Client disconnected: {client}")
                subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", client, "-j", "DROP"])

        connected_clients = active_clients
        time.sleep(5)

if __name__ == "__main__":
    wireless_interface = get_wireless_interface()
    print(wireless_interface)
    if wireless_interface:
        setup_hostapd(AP_SSID, AP_PASSPHRASE, wireless_interface)
        setup_dnsmasq(wireless_interface, DHCP_RANGE, DHCP_SUBNET)
        configure_network(wireless_interface)
        monitor_connections(wireless_interface)
    else:
        print("No wireless interface found")
