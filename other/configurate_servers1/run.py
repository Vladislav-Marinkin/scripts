from SSHClient import SSHClient
from UserDialog import UserDialog
from NetworkScanner import NetworkScanner
from SSHClient import SSHClient

if __name__ == "__main__":
    # Запрашиваем логин и пароль, ключ или указываем, что форма входа для каждого сервера будет разная
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # Сканируем сеть на наличие хостов
    ip = user_dialog.get_subnet_from_user()
    network_scanner = NetworkScanner(ip)
    network_servers = network_scanner.scan(user_dialog)

    # Записываем экземпляры класса SSHClient в лист servers
    servers = []
    for server in network_servers:
        if server['ssh']:
            ssh_client = SSHClient(server['ip'], user_dialog)
            ssh_client.connect_to_server()
            ssh_client.get_hostname_server()
            servers.append(ssh_client)

    # Выбираем нужные сервера
    servers = user_dialog.server_selection(servers)

    # Производим изменения на серверах
    if user_dialog.apply_changes():
        if user_dialog.change_netplan_config():
            for server in servers:
                server.change_netplan_config()

        if user_dialog.change_hostname():
            for server in servers:
                server.change_hostname(user_dialog)

        if user_dialog.modify_hosts_file():
            for server in servers:
                server.modify_hosts_file(servers)

    # Откат серверов
    if user_dialog.rollback_changes():
        for server in servers:
            server.rollback()

    # Перезагрузка серверов
    if user_dialog.reboot_server():
        for server in servers:
            server.reboot_server()

    # Закрываем все соединения
    for server in servers:
        server.close()