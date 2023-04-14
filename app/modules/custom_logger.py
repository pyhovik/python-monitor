import logging
from logging.handlers import SysLogHandler
from sys import stdout


def custom_logger(name,
                  console_handl = True,
                  file_handl = False,
                  syslog_handle = False,
                  log_path = f'{__name__}.log',
                  mode = 'w'):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if console_handl:
        console_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s (%(name)s): %(message)s"
            )
        console_handler = logging.StreamHandler(stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    if file_handl:
        file_handler = logging.FileHandler(log_path,
                                        encoding='utf-8',
                                        mode=mode)
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s (%(name)s): %(message)s"
            )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
    
    if syslog_handle:
        syslog_handler = SysLogHandler(address = '/dev/log')
        syslog_formatter = logging.Formatter(
            "(%(name)s) %(levelname)s: %(message)s"
            )
        syslog_handler.setFormatter(syslog_formatter)
        syslog_handler.setLevel(logging.WARNING)
        logger.addHandler(syslog_handler)

    return logger