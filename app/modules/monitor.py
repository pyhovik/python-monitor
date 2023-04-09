"""
Модуль, предоставляющий инструменты для мониторинга хоста.
"""

import psutil
import time
import logging
import schedule

from threading import Thread, Timer
from logging.handlers import SysLogHandler

# настройка логгирования
logger = logging.getLogger('monitor')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log', encoding='utf-8', mode='w')
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(name)s): %(message)s")
file_handler.setFormatter(file_formatter)

syslog_handler = SysLogHandler(address = '/dev/log')
syslog_formatter = logging.Formatter("(%(name)s) %(levelname)s: %(message)s")
syslog_handler.setFormatter(syslog_formatter)

logger.addHandler(file_handler)
logger.addHandler(syslog_handler)


class Monitor:
    """
    Класс предоставляет инструменты для интроспекции параметров системы.
    Класс опрашивает соответствующие параметры с заданной периодичностью и 
    отправляет данные в хранилище (файл, БД и проч.).
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def check_cpu_params(self, period = 10):
        print(period)
        while self.enabled:
            total_cpu_load = psutil.cpu_percent()
            logger.info(f'Total CPU usage (%) = {total_cpu_load};')
            time.sleep(period)
    
    def check_mem_params(self):
        free_ram = psutil.virtual_memory().free
        logger.info(f'Free MEM = {free_ram};')
        
    def start(self, period: int = 20):
        #self.enabled = True
        schedule.every(period).seconds.do(self.check_cpu_params)
        schedule.every(period).seconds.do(self.check_mem_params)
        
        while self.enabled:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        self.enabled = False

    



if __name__ == '__main__':
    monitor = Monitor()
    thrd = Thread(target=monitor.check_cpu_params, args=[5])
    thrd.start()
    print('next')
    import random
    while 1:
        time.sleep(5)
        if random.randint(1,4) == 1:
            break
        print('wait')
    monitor.stop()
