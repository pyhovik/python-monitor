"""
Модуль, предоставляющий инструменты для сбора информации о целевом хосте:
информация о системе, окружении и проч.
"""

import os
import psutil
import cpuinfo
import platform
import json
from subprocess import check_output


class Inspector:
    """
    Класс предоставляет инструменты для инвентаризации системы
    """
    def __init__(self):
        if platform.system() == 'Linux':
            self.get_os_info()
            self.get_cpu_info()
            self.get_mem_info()
            self.get_motherboard_info()
            self.get_disk_info()
        else:
            print('Unsupported platform!')

    def get_os_info(self):
        """Метод, собирающий инф-цию о ОС."""
        self.os = {}
        self.os['hostname'] = os.uname().nodename
        self.os['release'] = check_output(
            'lsb_release -d', 
            encoding='utf-8', 
            shell=True
            ).split(':')[1].strip()
    
    def get_cpu_info(self):
        """Собирает инф-цию о ЦПУ."""
        self.cpu = {}
        self.cpu['model'] = cpuinfo.get_cpu_info()['brand_raw']
        self.cpu['ph_core'] = psutil.cpu_count(logical=False)
        self.cpu['lg_core'] = psutil.cpu_count()
    
    def get_mem_info(self):
        """Собирает инф-цию о ОЗУ и SWAP."""
        Gb_sufix = 1024 ** 3
        self.mem = {}
        ram_total_Gb = psutil.virtual_memory().total / Gb_sufix
        swap_total_Gb = psutil.swap_memory().total / Gb_sufix
        self.mem['ram_total'] = f"{ram_total_Gb:.1f}Gb"
        self.mem['swap_total'] = f"{swap_total_Gb:.1f}Gb"                              
    
    def get_motherboard_info(self):
        """Собирает инф-2ию о мат. плате"""
        self.mb = {}
        self.mb['name'] = check_output(
            "cat /sys/devices/virtual/dmi/id/board_name", 
            encoding='utf-8', 
            shell=True
            ).rstrip()
        self.mb['vendor'] = check_output(
            "cat /sys/devices/virtual/dmi/id/board_vendor", 
            encoding='utf-8', 
            shell=True
            ).rstrip()
    
    def get_disk_info(self):
        """Собирает инф-цию о дисках."""
        out = check_output(
            "lsblk -o +model -J", 
            encoding='utf-8', 
            shell=True
            )
        self.disks = []
        jout = json.loads(out)
        # в цикле проходимся по выводу и "собираем" дискиы
        for device in jout['blockdevices']:
            if device['type'] == 'disk':
                self.disks.append([
                        device['name'],
                        device['size'],
                        device['model']
                    ]
                )
  
    def show_params(self):
        """Печатает все доступные параметры в консоль."""
        for attr in self.__dict__.keys():
            print(f"{attr} => {self.__dict__[attr]}")
    
    def export_to_dict(self):
        """Метод, возвразающий все параметры системы в JSON-объекте."""
        params = {
            'OS': self.os,
            'Motherboar': self.mb,
            'CPU': self.cpu,
            'Memory': self.mem,
            'Disks': self.disks
        }
        return params


if __name__ == '__main__':
    inspector = Inspector()
    inspector.show_params()
    print(inspector.export_to_dict())
