# ADr3c0n
ADr3c0n - Active Directory Recon Tool

ADr3c0n is an Active Directory reconnaissance tool designed to help security professionals and penetration testers gather information about Active Directory environments. The tool performs various reconnaissance tasks, such as listing domain administrators, enumerating users, conducting Kerberoasting and AS-REP roasting, and performing host reconnaissance.

Features

List Active Directory domain administrators

Enumerate all users in the Active Directory environment

Perform Kerberoasting attacks (future implementation)

Perform AS-REP Roasting attacks (future implementation)

Conduct host reconnaissance, including ping sweeps, port scanning, and service banner grabbing

Configurable via a YAML file for easy customization

Requirements

Python 3.7+

Required Python Libraries:

argparse

yaml

logging

socket

subprocess

concurrent.futures

ldap3

colorama

To install dependencies, run:

pip install -r requirements.txt

Installation

Clone the repository:

git clone https://github.com/yourusername/ADr3c0n.git
cd ADr3c0n

Install dependencies:

pip install -r requirements.txt

Configure conf.yaml with your LDAP settings:

# Configuration file for ADr3c0n

# LDAP server settings
server_ip: "192.168.1.1"  # Replace with the IP address of your LDAP server
username: "your_username" # Replace with your LDAP username
password: "your_password" # Replace with your LDAP password

# Operations to perform
list_admins: true    # Set to true to list domain admins
list_users: true     # Set to true to list all users
kerberoast: true    # Set to true to perform Kerberoasting
asrep_roast: true   # Set to true to perform AS-REP Roasting
host_recon: true     # Set to true to perform host reconnaissance

# Host reconnaissance settings
host_ip: "192.168.1.100"  # Replace with the IP address you want to scan

Usage

Run the tool with a configuration file:

python3 ADr3c0n.py --conf conf.yaml

Output Example

Performing Active Directory Recon...
[+] Domain Admins:
    - Administrator
    - AdminUser
[+] Users:
    - user1
    - user2
    - user3
[+] Performing host reconnaissance on 192.168.1.100...
    - 192.168.1.100 is up.
    - Open ports: 80, 445, 3389
    - Port 80 banner: Apache/2.4.41 (Ubuntu)
    - Port 445 banner: Microsoft-DS

Roadmap

Implement Kerberoasting and AS-REP Roasting functionalities

Enhance LDAP enumeration capabilities

Add additional scanning techniques for host reconnaissance

Improve error handling and logging

Disclaimer

This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use of this tool on networks without permission may be illegal. Use responsibly.

License

MIT License
