"""
Модуль, предоставляющий инструменты для сбора информации о целевом хосте:
информация о системе, окружении и проч.
"""

import os
from subprocess import check_output

def commandExec(cmd: str) -> str:
    return check_output

class Inspector:
    """
    Класс предоставляет инструменты для инвентаризации системы
    """
    def __init__(self):
        self.getOsInfo()
    def getOsInfo(self):
        self.hostname = check_output('cat /etc/hostname', 
                                    encoding='utf-8', 
                                    shell=True).rstrip()
        self.os_info = check_output('lsb_release -d', 
                                    encoding='utf-8', 
                                    shell=True).split(':')[1].strip()
        self.cpu_model = check_output("cat /proc/cpuinfo | grep 'model name' -m1", 
                                    encoding='utf-8', 
                                    shell=True).split(':')[1].strip()
    def getCpuInfi(self): pass
    def getMemInfo(self): pass
    def getMotherboardInfo(self): pass
    def showParams(self):
        for attr in self.__dict__.keys():
            print(f"{attr} => {self.__dict__[attr]}")

if __name__ == '__main__':
    inventor = Inspector()
    inventor.showParams()