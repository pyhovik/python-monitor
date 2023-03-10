"""
Модуль, предоставляющий инструменты для сбора информации о целевом хосте:
информация о системе, окружении и проч.
"""

import os
import re
import json
from subprocess import check_output


class Inspector:
    """
    Класс предоставляет инструменты для инвентаризации системы
    """
    def __init__(self):
        self.getOsInfo()
        self.getCpuInfo()
        self.getMemInfo()
        self.getMotherboardInfo()
        self.getDiskInfo()

    def getOsInfo(self):
        """Метод, собирающий инф-цию о ОС"""
        self.hostname = check_output(
            'cat /etc/hostname', 
            encoding='utf-8', 
            shell=True
            ).rstrip()
        self.os_info = check_output(
            'lsb_release -d', 
            encoding='utf-8', 
            shell=True
            ).split(':')[1].strip()
    
    def getCpuInfo(self):
        """Собирает инф-цию о ЦПУ"""
        self.cpu_model = check_output(
            "cat /proc/cpuinfo | grep 'model name' -m1", 
            encoding='utf-8', 
            shell=True
            ).split(':')[1].strip()
    
    def getMemInfo(self):
        """Собирает инф-2ию о ОЗУ и свап"""
        self.mem_total = check_output(
            "free --giga | grep Mem | awk '{print $2}'", 
            encoding='utf-8', 
            shell=True
            ).strip()
        self.swap_total = check_output(
            "free --giga | grep Swap | awk '{print $2}'", 
            encoding='utf-8', 
            shell=True
            ).strip()                                   
    
    def getMotherboardInfo(self):
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
    
    def getDiskInfo(self):
        """собирает инф-2ию о дисках"""
        out = check_output(
            "lsblk -J", 
            encoding='utf-8', 
            shell=True
            )
        self.disks = []
        jout = json.loads(out)
        # в цикле проходимся по выводу и "собираем" дискиы
        for device in jout['blockdevices']:
            if device['type'] == 'disk':
                self.disks.append(dict(
                        diskName = device['name'],
                        diskSize = device['size']
                    )
                )

              
    def showOsInfo(self): pass
    def showCpuInfo(self): pass
    def showMemInfo(self): pass
    def showParams(self):
        for attr in self.__dict__.keys():
            print(f"{attr} => {self.__dict__[attr]}")
    def __str__(self):
        return "Inspector"

if __name__ == '__main__':
    inspector = Inspector()
    print(inspector.disks)
    inspector.showParams()