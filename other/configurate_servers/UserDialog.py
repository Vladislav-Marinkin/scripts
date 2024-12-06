import ipaddress
import getpass
import os
import select
from sys import platform
from wsgiref import validate

class UserDialog(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.sudo_password = None
        self.key_filename = None
        self.use_login_password_separately = False

    def check_yes_no(self, answer):
        while True:
            use_login_password = input(answer).lower()
            if use_login_password in ('yes', 'no'):
                if use_login_password == 'yes':
                    return True
                else:
                    return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def prompt_login_credentials(self, hostname = None):
        if self.use_login_password_separately != True:
            while True:
                use_login_password_separately = input("Will the input of username and password be performed for each server separately? (yes/no): ").lower()
                if use_login_password_separately in ('yes', 'no'):
                    if use_login_password_separately == 'yes':
                        self.use_login_password_separately = True
                        return
                    else:
                        self.use_login_password_separately = False
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        if self.check_yes_no("Do you want to use login/password? (yes/no): "):
            self.username = input("Username: ")
            self.password = getpass.getpass("Password: ")
            while True:
                sudo_password = input("Is the entered password different from the superuser password? (yes/no): ")
                if sudo_password in ('yes', 'no'):
                    if sudo_password == 'yes':
                        self.sudo_password = self.password
                        break
                    else:
                        self.sudo_password = getpass.getpass("Superuser password: ")
                        break
        else:
            self.key_filename = input("Path to private key file: ")
            self.username = input("Username: ")
            self.sudo_password = getpass.getpass("Superuser password: ")


    def validate_ip(self, ip_address):
        try:
            ipaddress.IPv4Address(ip_address)
            return True
        except ipaddress.AddressValueError:
            return False

    def enter_new_ip(self, hostname):
        print(f"Enter new ip addres for {hostname}")

        while True:
            ip = input("Enter you new ip: ")

            if self.validate_ip(ip):
                return ip
            else:
                print("The IP address is entered incorrectly, try entering it again.")

    def get_subnet_from_user(self):
        while True:
            ip = input("Enter the network for scanning (e.g., '192.168.0.1'): ")

            if self.validate_ip(ip):
                return ip + "/24"
            else:
                print("The IP address is entered incorrectly, try entering it again.")

    def clear_console(self):
        if platform.startswith('win'):
            os.system('cls')
        elif platform.startswith('linux') or platform.startswith('darwin'):
            os.system('clear')

    def server_selection(self, servers):
        self.clear_console()

        i = 0
        for server in servers:
            i += 1
            print(f"{i}) IP: {server.ip}, Hostname: {server.hostname}")

        while True:
            try:
                select_servers = list(map(int, input("Enter number servers (e.g., 1,2,3): ").split(',')))

                if not select_servers:
                    raise ValueError("Please enter at least one server number.")

                print("Selected servers:", select_servers)

                break

            except ValueError as e:
                print(f"Error: {e}. Please enter valid server numbers.")

        selected_servers = []

        for server_index in select_servers:
            if 1 <= server_index <= len(servers):
                selected_servers.append(servers[server_index - 1])

        not_selected_servers = set(servers) - set(selected_servers)
        for server in not_selected_servers:
            server.close()

        return selected_servers

    def rollback_changes(self):
        if self.check_yes_no("Do you want to roll back all changes? (yes/no): "):
            return True
        else:
            return False

    def apply_changes(self):
        if self.check_yes_no("Do you want to change server settings? (yes/no): "):
            return True
        else:
            return False

    def get_user_hostname(self, ip):
        while True:
            hostname = input("Please enter your hostname: ")

            if self.check_yes_no(f"Set the provided {hostname} for the server at {ip}? (yes/no): "):
                return hostname

    def reboot_server(self):
        if self.check_yes_no("Do you want to reboot all servers? (yes/no): "):
            return True
        else:
            return False

    def retry_connection(self):
        if self.check_yes_no("Retry the connection to the server? (yes/no): "):
            return True
        else:
            return False

    def change_netplan_config(self):
        if self.check_yes_no("Do you want to change netplan config? (yes/no): "):
            return True
        else:
            return False

    def change_hostname(self):
        if self.check_yes_no("Do you want to change hostname? (yes/no): "):
            return True
        else:
            return False

    def modify_hosts_file(self):
        if self.check_yes_no("Do you want to change hosts file? (yes/no): "):
            return True
        else:
            return False