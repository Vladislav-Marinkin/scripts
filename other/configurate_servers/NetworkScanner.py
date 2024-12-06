import socket
from scapy.all import ARP, Ether, srp

class NetworkScanner(object):
    def __init__(self, ip):
        self.ip = ip

    def scan(self, user_dialog):
        while True:
            arp_request = ARP(pdst=self.ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

            client_list = []
            for i in range(0, len(answered_list)):
                client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
                client_dict["ssh"] = self.check_ssh(answered_list[i][1].psrc)
                client_list.append(client_dict)

            for server in client_list:
                print(f"{server['ip']}, {server['mac']}")

            if user_dialog.check_yes_no("Scan the network again? (yes/no): ") == False:
                return client_list

    def check_ssh(self, ip, port=22, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, port))
            sock.close()
            return True
        except:
            return False




