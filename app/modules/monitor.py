"""
Модуль, предоставляющий инструменты для мониторинга хоста.
"""

import psutil
import time
import threading
from custom_logger import custom_logger

logger = custom_logger('monitor')


class Monitor:
    """
    Класс предоставляет инструменты для интроспекции параметров системы.
    Класс опрашивает соответствующие параметры с заданной периодичностью и 
    отправляет данные в хранилище (файл, БД и проч.).
    """

    def __init__(self, enabled: bool = True, period: int = 10):
        self.enabled = enabled
        self.period = period

    def _check_cpu_params(self):
        while self.enabled:
            total_cpu_load = psutil.cpu_percent()
            logger.info(f'Total CPU usage (%) = {total_cpu_load}.')
            time.sleep(self.period)
    
    def _check_mem_params(self):
        while self.enabled:
            free_ram = psutil.virtual_memory().free
            logger.info(f'Free MEM = {free_ram}.')
            time.sleep(self.period)

    def start(self):
        self.enabled = True
        logger.info(f'Starting monitoring...')
        # запуск функций в потоках
        for meth in [m for m in dir(self) if m.startswith('_check')]:
            meth = getattr(self, meth)
            threading.Thread(target=meth).start()
        time.sleep(1)
        logger.info(f'Monitoring started.')

    def stop(self):
        self.enabled = False
        time.sleep(self.period)
        logger.info(f'Monitoring stopped.')

