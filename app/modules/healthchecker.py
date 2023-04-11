"""
Модуль, предоставляющий инструменты для опроса состояния серверов.
"""

import telebot
from icmplib import multiping
from .custom_logger import custom_logger
from influxdb_client import InfluxDBClient, Point


class ChangeServerStatus(Exception): pass


class Healthchecker:
    """
    Класс предоставляет инструменты для опроса статусов серверов.
    """
    def __init__(self,
                 path_to_server_list: str,
                 bot_token = None,
                 chad_id = None,
                 influx_token = None,
                 influx_bucket = None,
                 influx_org = None,
                 influx_server = None,
                 log_path = 'healhcheck.log',
                 log_mode = 'w'):
        
        self.servers = {}
        with open(path_to_server_list) as f:
            for line in f:
                server = line.split()
                self.servers[server[1]] = {
                    'hostname': server[0],
                    'status': True
                }
        self.servers_ip = list(self.servers.keys())
        self.unavailable_servers = []

        # если есть параметры - инициализируем клиента БД
        if influx_server:
            self._influx_client = InfluxDBClient(
                                    url=f"http://{influx_server}:8086",
                                    token=influx_token,
                                    org=influx_org)
            self._influx_bucket = influx_bucket
            self._influx_org = influx_org
            self._write_api = self._influx_client.write_api()
            self._influx_enabled = True
        else:
            self._influx_enabled = False

        if bot_token:
            self._bot = telebot.TeleBot(bot_token)
            self._chat_id = chad_id
            self._bot_enabled = True
        else:
            self._bot_enabled = False
        
        self._logger = custom_logger('healhcheck', log_path, log_mode)

    def check_servers_status(self):
        try:
            hosts = multiping(
                addresses=self.servers_ip,
                timeout=2,
                privileged=False
            )
            # обновляем информацию
            status_changed = False
            changed_servers = []
            for host in hosts:
                status_before = self.servers[host.address]['status']
                actual_status = host.is_alive
                self.servers[host.address]['status'] = actual_status
                # если произошла смена статуса...
                if status_before != actual_status:
                    status_changed = True
                    if actual_status == False:
                        self.unavailable_servers.append(host.address)
                    elif actual_status == True:
                        self.unavailable_servers.remove(host.address)
                    changed_servers.append(
                        (
                            host.address,
                            self.servers[host.address]['hostname'],
                            'UP' if actual_status else 'DOWN'
                        )
                    )
                # пишем в базу
                if self._influx_enabled:
                    host=self.servers[host.address]['hostname']
                    point = Point("servers_status")
                    point.tag('host', host)
                    point.field('status', int(actual_status))
                    self._write_api.write(self._influx_bucket,
                                        self._influx_org,
                                        point)
            # если есть изменения - генерируем исключение
            if status_changed:
                raise ChangeServerStatus(changed_servers)
        except ChangeServerStatus as e:
            text_err = f'ALERT! Servers changed its status!\n'
            for (addr, hostname, status) in e.args[0]:
                text_err += f"{hostname} ({addr}) -> {status}\n"
            self._logger.error(text_err)
            if self._bot_enabled:
                self._bot.send_message(chat_id=self._chat_id,
                                       text=text_err)
        else:
            if self.unavailable_servers:
                self._logger.warning(
                    f'Some servers have status DOWN: {self.unavailable_servers}')
            else:
                self._logger.info('All servers have status UP.')

    def notify_server_status(self):
        notification = "Current servers status:\n"
        for addr in self.servers:
            hostname = self.servers[addr]['hostname']
            status = 'UP' if self.servers[addr]['status'] else 'DOWN'
            notification += f"{hostname} ({addr} - {status})\n"
        if self._bot_enabled:
            self._bot.send_message(chat_id=self._chat_id,
                                    text=notification)
