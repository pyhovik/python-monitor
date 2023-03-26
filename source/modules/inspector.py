"""
Модуль, предоставляющий инструменты для сбора информации о целевом хосте:
информация о системе, окружении и проч.
"""

import json
import os
import psutil
import cpuinfo
import platform
from subprocess import check_output, CalledProcessError


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
        self.os_hostname = os.uname().nodename
        self.os_release = check_output(
            'lsb_release -d', 
            encoding='utf-8', 
            shell=True
            ).split(':')[1].strip()
    
    def get_cpu_info(self):
        """Собирает инф-цию о ЦПУ."""
        self.cpu_model = cpuinfo.get_cpu_info()['brand_raw']
        self.cpu_ph_core = psutil.cpu_count(logical=False)
        self.cpu_lg_core = psutil.cpu_count()
    
    def get_mem_info(self):
        """Собирает инф-цию о ОЗУ и SWAP."""
        Gb_sufix = 1024 ** 3
        ram_total_Gb = psutil.virtual_memory().total / Gb_sufix
        swap_total_Gb = psutil.swap_memory().total / Gb_sufix
        self.mem_ram_total = f"{ram_total_Gb:.1f}Gb"
        self.mem_swap_total = f"{swap_total_Gb:.1f}Gb"                              
    
    def get_motherboard_info(self):
        """Собирает инф-2ию о мат. плате"""
        self.mb_name = check_output(
            "cat /sys/devices/virtual/dmi/id/board_name", 
            encoding='utf-8', 
            shell=True
            ).rstrip()
        self.mb_vendor = check_output(
            "cat /sys/devices/virtual/dmi/id/board_vendor", 
            encoding='utf-8', 
            shell=True
            ).rstrip()
    
    def get_disk_info(self):
        """Собирает инф-2ию о дисках."""
        out = check_output(
            "lsblk -J", 
            encoding='utf-8', 
            shell=True
            )
        self.disks = []
        jout = json.loads(out)
        # в цикле проходимся по выводу и "собираем" диски
        for device in jout['blockdevices']:
            if device['type'] == 'disk':
                self.disks.append(dict(
                        blockdev = device['name'],
                        size = device['size']
                    )
                )
        # определить модель для каждого диска
        try:
            for disk in self.disks:
                model = check_output(
                f"sudo fdisk -l /dev/{disk['blockdev']} 2>&1 | grep model", 
                encoding='utf-8', 
                shell=True
                ).split(':')[1].strip()
                disk['model'] = model
        except CalledProcessError:
            print('Cannot get disk model - Permission denied.')
        
    def show_params(self):
        """Печатает все доступные параметры в консоль."""
        for attr in self.__dict__.keys():
            print(f"{attr} => {self.__dict__[attr]}")
    
    def export_to_dict(self):
        """Метод, возвразающий все параметры системы в JSON-объекте."""
        params = {
            'OS': {
                'hosntame': self.os_hostname,
                'release': self.os_release
            },
            'CPU': {
                'core_physical': self.cpu_ph_core,
                'core_logical': self.cpu_lg_core,
                'model': self.cpu_model
            },
            'Memory': {
              'ram_total': self.mem_ram_total,
              'swap_total': self.mem_swap_total  
            },
            'Motherboard': {
                'name': self.mb_name,
                'vendor': self.mb_vendor
            },
            'Disks': self.disks
        }
        return params


if __name__ == '__main__':
    inspector = Inspector()
    inspector.show_params()