"""
Модуль, предоставляющий инструменты для опроса состояния серверов.
"""

import subprocess
import time


class Healthchecker:
    """
    Класс предоставляет инструменты для опроса статусов серверов.
    """
    def __init__(self, server_list):
        self.servers = {}
        with open(path) as f:
            for line in f:
                server = line.split()
                self.servers[server[0]] = server[1]
        self.hostnames = [name for name in self.servers]

    def update_server_status(self, hostname, attempts = 3):
        ip = self.servers[hostname]
        command = f'ping -c2 -W1 {ip} >/dev/null'
        for _ in range(attempts):
            result_code = subprocess.call(command, shell=True)
            if result_code == 0: break
        return result_code

def check_servers_status(path: str, attempts: int = 3) -> dict:
    servers = get_server_list(path)
    servers_status = {}
    for hostname in servers:
        status = get_server_status(servers[hostname], attempts)
        servers_status[hostname] = status
        status = 'DOWN' if status == 1 else 'UP'
        servers_status[hostname] = status
    return servers_status


if __name__ == '__main__':
    path = 'app/configs/servers_for_checking.txt'
    start = time.time()
    statuses = check_servers_status(path)
    delta = time.time() - start
    print(statuses)
    print(delta)
