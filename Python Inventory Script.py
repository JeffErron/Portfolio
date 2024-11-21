import netmiko
import pandas as pd
import os

# Define the switch IP addresses, including 10.10.1.3
switch_ips = ["10.10.1.3", "10.10.1.5", "10.10.1.6", "10.10.1.7", "10.10.1.8"]

# Define the device type and credentials
device_type = "extreme_exos"
username = "admin"
password = ""  # No password

# Define the command to retrieve the necessary information
general_settings_command = "show version"
network_settings_command = "show ports information detail"

# Function to retrieve switch information
def get_switch_info(ip):
    device = {
        "device_type": device_type,
        "ip": ip,
        "username": username,
        "password": password,
    }
    try:
        connection = netmiko.ConnectHandler(**device)
        general_settings = connection.send_command(general_settings_command)
        network_settings = connection.send_command(network_settings_command)
        connection.disconnect()
        
        return general_settings, network_settings
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
        return None, None

# Collect information from all switches
switch_data = []
for ip in switch_ips:
    general_info, network_info = get_switch_info(ip)
    if general_info and network_info:
        switch_data.append({
            "IP Address": ip,
            "General Settings": general_info,
            "Network Settings": network_info
        })

# Convert the data to a DataFrame
df = pd.DataFrame(switch_data)

# Determine the path to the Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "switch_inventory.txt")

# Save the DataFrame to a text file on the Desktop
df.to_csv(desktop_path, sep='\t', index=False)

print(f"Switch inventory has been saved to {desktop_path}")