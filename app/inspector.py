"""
Модуль, предоставляющий инструменты для сбора информации о целевом хосте:
информация о системе, окружении и проч.
"""

import os
import re
from subprocess import check_output


class Inspector:
    """
    Класс предоставляет инструменты для инвентаризации системы
    """
    def __init__(self):
        self.getOsInfo()
        self.getCpuInfo()

    def getOsInfo(self):
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
        self.cpu_model = check_output(
            "cat /proc/cpuinfo | grep 'model name' -m1", 
            encoding='utf-8', 
            shell=True
            ).split(':')[1].strip()
    
    def getMemInfo(self):
        self.mem_total = check_output(
            "free --mega | grep Mem | awk '{print $2}'", 
            encoding='utf-8', 
            shell=True
            ).strip()
        self.swap_total = check_output(
            "free --mega | grep Swap | awk '{print $2}'", 
            encoding='utf-8', 
            shell=True
            ).strip()                                   
    
    def getMotherboardInfo(self):
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
    
    def getRomInfo(self):
        disks = check_output(
            "lsblk -o NAME,SIZE,TYPE | grep disk", 
            encoding='utf-8', 
            shell=True
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
    inspector.showParams()
    print(inspector)