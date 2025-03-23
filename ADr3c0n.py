import argparse
import yaml
import logging
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
from ldap3 import Server, Connection, ALL, NTLM

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_file):
    """Load configuration from YAML file."""
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def connect_ldap(server_ip, username, password):
    """Establish an LDAP connection."""
    server = Server(server_ip, get_info=ALL)
    conn = Connection(server, user=username, password=password, authentication=NTLM)
    if not conn.bind():
        logger.error("Failed to bind to LDAP server.")
        raise Exception("LDAP bind failed")
    return conn

def list_domain_admins(conn):
    """List domain admins."""
    search_filter = '(memberOf:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=example,DC=com)'
    conn.search('CN=Users,DC=example,DC=com', search_filter, attributes=['cn'])
    for entry in conn.entries:
        print(f'Domain Admin: {entry.cn}')

def list_users(conn):
    """List all users."""
    conn.search('CN=Users,DC=example,DC=com', '(objectClass=user)', attributes=['cn'])
    for entry in conn.entries:
        print(f'User: {entry.cn}')

def kerberoast(conn):
    """Perform Kerberoasting."""
    # Placeholder for Kerberoasting functionality
    print('Kerberoasting functionality not yet implemented.')

def asrep_roast(conn):
    """Perform AS-REP Roasting."""
    # Placeholder for AS-REP roasting functionality
    print('AS-REP roasting functionality not yet implemented.')

def host_recon(server_ip):
    """Perform host reconnaissance."""
    print(f'Performing host reconnaissance on {server_ip}...')
    
    # Ping Scan
    if ping_host(server_ip):
        print(f'{server_ip} is up.')
    else:
        print(f'{server_ip} is down or not reachable.')
        return

    # Port Scan
    open_ports = scan_ports(server_ip)
    if open_ports:
        print(f'Open ports on {server_ip}: {", ".join(map(str, open_ports))}')
        for port in open_ports:
            banner = grab_service_banner(server_ip, port)
            print(f'Port {port} banner: {banner}')
    else:
        print('No open ports found.')

def ping_host(host):
    """Check if a host is up using ICMP ping."""
    try:
        # Linux/Mac: use 'ping -c 1'
        # Windows: use 'ping -n 1'
        subprocess.check_call(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def scan_ports(host):
    """Scan for open ports on a host."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, host, port) for port in range(1, 1025)]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return open_ports

def check_port(host, port):
    """Check if a specific port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((host, port))
            return port, True
        except (socket.timeout, socket.error):
            return port, False

def grab_service_banner(host, port):
    """Grab the service banner from an open port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((host, port))
            banner = sock.recv(1024).decode('utf-8').strip()
            return banner
    except Exception as e:
        logger.error(f"Error grabbing banner: {e}")
        return 'No banner'

def perform_ad_operations(conn, config):
    """Perform AD operations based on configuration."""
    if config.get('list_admins', False):
        list_domain_admins(conn)
    if config.get('list_users', False):
        list_users(conn)
    if config.get('kerberoast', False):
        kerberoast(conn)
    if config.get('asrep_roast', False):
        asrep_roast(conn)
    if config.get('host_recon', False):
        host_recon(config['server_ip'])

def main(args):

    config = load_config(args.conf)
    
    try:
        conn = connect_ldap(config['server_ip'], config['username'], config['password'])
        perform_ad_operations(conn, config)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        conn.unbind()

if __name__ == '__main__':
    import colorama
    from colorama import Fore, Style
    
    
    print(
        Fore.GREEN +
        "   ___     ___             ____             __             \n"
        "  /   \\   |   \\     _ _   |__ /    __      /  \\   _ _     \n"
        "  | - |   | |) |   | '_|   |_ \\   / _|    | () | | ' \\    \n"
        "  |_|_|   |___/   _|_|_   |___/   \\__|_   _\\__/  |_||_|   \n"
        " _|\"\"\"\"\"|_|\"\"\"\"|_|\"\"\"\"|_|\"\"\"\"|_|\"\"\"\"|_|\"\"\"\"|_|\"\"\"\"|_|   \n"
        "\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'"
        + Style.RESET_ALL
    )
    
    print('		'*20)
    parser = argparse.ArgumentParser(description='ADr3c0n: Active Directory Recon Tool')
    parser.add_argument('--conf', required=True, help='Path to configuration file (YAML)')
    
    args = parser.parse_args()
    main(args)






