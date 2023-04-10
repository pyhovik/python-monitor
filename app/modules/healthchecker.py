"""
Модуль, предоставляющий инструменты для опроса состояния серверов.
"""

import time
import telebot
from icmplib import multiping
from custom_logger import custom_logger
from threading import Thread
from influxdb_client import InfluxDBClient, Point
from pyhocon import ConfigFactory

conf = ConfigFactory.parse_file('hocon.conf')
bot_token = conf.get('notification.telegram.token')
chat_id = conf.get('notification.telegram.chat_id')
bot = telebot.TeleBot(bot_token)

influx_token = conf.get('influxdb.influx_token')
bucket = conf.get('influxdb.bucket')
org = conf.get('influxdb.org')
influx_server = conf.get('influxdb.server')
influx_client = InfluxDBClient(url=f"http://{influx_server}:8086",
                                        token=influx_token,
                                        org=org)
write_api = influx_client.write_api()
query_api = influx_client.query_api()

path_to_server_list = conf.get('servers.path_to_list')
timeout = conf.get('monitoring.timeout')
notify_time = conf.get('monitoring.notify_time')

log_path = conf.get('notification.logging.log_path')
log_mode = conf.get('notification.logging.log_mode')
logger = custom_logger('healhcheck', log_path, log_mode)


class ChangeServerStatus(Exception): pass


class Healthchecker:
    """
    Класс предоставляет инструменты для опроса статусов серверов.
    """
    def __init__(self,
                 path_to_list: str,
                 timeout: int = 200):
        self.timeout = timeout
        self.enabled = False
        self.servers = {}
        self.unavailable_servers = []
        with open(path_to_list) as f:
            for line in f:
                server = line.split()
                self.servers[server[1]] = {
                    'hostname': server[0],
                    'status': True
                }
        self.servers_ip = list(self.servers.keys())

    def check_servers_status(self) -> dict:
        while self.enabled:
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
                    host=self.servers[host.address]['hostname']
                    point = Point("servers_status")
                    point.tag('host', host)
                    point.field('status', int(actual_status))
                    write_api.write(bucket, org, point)

                time.sleep(self.timeout)
                # если есть изменения - генерируем исключение
                if status_changed:
                    raise ChangeServerStatus(changed_servers)

            except ChangeServerStatus as e:
                text_err = f'ALERT! Servers changed its status!\n'
                for (addr, hostname, status) in e.args[0]:
                    text_err += f"{hostname} ({addr}) -> {status}\n"
                logger.error(text_err)
                bot.send_message(chat_id=chat_id,
                                 text=text_err)
            else:
                if self.unavailable_servers:
                    logger.warning(
                        f'Some servers have status DOWN: {self.unavailable_servers}')
                else:
                    logger.info('All servers have status UP.')

    def notify_server_status(self):
        while self.enabled:
            now = time.strftime('%H:%M')
            if now == notify_time:
                notification = "Current servers status:\n"
                for addr in self.servers:
                    hostname = self.servers[addr]['hostname']
                    status = 'UP' if self.servers[addr]['status'] else 'DOWN'
                    notification += f"{hostname} ({addr} - {status})\n"
                bot.send_message(chat_id=chat_id,
                                 text=notification)
            logger.info(f'from notify {now}')
            time.sleep(30)

    def start(self):
        self.enabled = True
        thr1 = Thread(target=self.check_servers_status, daemon=True)
        thr1.start()
        logger.info('Healt checking started.')
        thr2 = Thread(target=self.notify_server_status, daemon=True)
        thr2.start()
        logger.info('Notify daemon started.')
        thr1.join()

    def stop(self):
        self.enabled = False
        logger.info('Health checking stopped.')


if __name__ == '__main__':
    hc = Healthchecker(path_to_server_list, timeout)
    hc.start()
    # while 1:
    #     flag = input("Ввод (start/stop/exit/info): ")
    #     if flag == 'stop':
    #         hc.stop()
    #     elif flag == 'start':
    #         hc.start()
    #     elif flag == 'exit':
    #         hc.stop()
    #         break
    #     elif flag == 'info':
    #         print(hc.servers)
    #         print(hc.enabled)

