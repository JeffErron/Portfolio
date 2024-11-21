import netmiko

# Define the switch IP addresses (excluding 10.10.1.3)
switch_ips = ["10.10.1.5", "10.10.1.6", "10.10.1.7", "10.10.1.8"]

# Define the device type and credentials
device_type = "extreme_exos"
username = "admin"
password = ""  # No password

# VLANs to be configured
vlans = [
    {"name": "User_Network", "id": 10},
    {"name": "ACCT_Network", "id": 20},
    {"name": "MGMT_Network", "id": 30},
    {"name": "IT_Network", "id": 40},
]

# Function to configure VLANs on a switch
def configure_vlans(ip):
    device = {
        "device_type": device_type,
        "ip": ip,
        "username": username,
        "password": password,
    }
    try:
        connection = netmiko.ConnectHandler(**device)
        for vlan in vlans:
            commands = [
                f"create vlan {vlan['name']} tag {vlan['id']}",
                f"configure vlan {vlan['name']} add ports all"
            ]
            connection.send_config_set(commands)
        connection.save_config()
        connection.disconnect()
        print(f"Configured VLANs on {ip} successfully.")
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")

# Configure VLANs on all switches
for ip in switch_ips:
    configure_vlans(ip)