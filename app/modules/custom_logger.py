import logging
from logging.handlers import SysLogHandler
from sys import stdout


def custom_logger(name, log_path = 'app.log', mode = 'w'):

    file_handler = logging.FileHandler(log_path,
                                       encoding='utf-8',
                                       mode=mode)
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s (%(name)s): %(message)s"
        )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    syslog_handler = SysLogHandler(address = '/dev/log')
    syslog_formatter = logging.Formatter(
        "(%(name)s) %(levelname)s: %(message)s"
        )
    syslog_handler.setFormatter(syslog_formatter)
    syslog_handler.setLevel(logging.WARNING)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    #logger.addHandler(syslog_handler)

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    
    return logger