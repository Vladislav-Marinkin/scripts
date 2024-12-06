import argparse

class ARGParse(object):
    def __init__(self):
        self.login = None
        self.password = None
        self.subnet = None
        
    def parse(self):
        parser = argparse.ArgumentParser(description='Script for managing servers over SSH.')
        parser.add_argument('-l', '--login', type=str, help='SSH login username')
        parser.add_argument('-p', '--password', type=str, help='SSH login password')
        parser.add_argument('-s', '--subnet', type=str, help='Subnet to scan for servers (e.g., 192.168.1.0/24)')

        args = parser.parse_args()
        
        if not (args.login or args.password or args.subnet):
            return False
        
        if args.login and args.password and args.subnet:
            self.login = args.login
            self.password = args.password
            self.subnet = args.subnet
            return True
        else:
            parser.print_help()
            exit(1)