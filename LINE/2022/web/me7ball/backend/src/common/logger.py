import os
import sys
from logging import getLogger, Formatter, StreamHandler, WARN, INFO, DEBUG
from logging.handlers import TimedRotatingFileHandler


def get_common_logger(name: str, log_level: str = "DEBUG", log_file_path: str = None, std_out: bool = True, backup_count: int = 180):
    """
    :param name:
    :param log_level:
    :param log_file_path:
    :param std_out:
    :param backup_count:
    :return:
    """
    logger = getLogger(name)
    if log_level == "WARN":
        log_level = WARN
    elif log_level == "INFO":
        log_level = INFO
    else:
        log_level = DEBUG

    formatter = Formatter("%(asctime)s %(levelname)s %(module)s %(lineno)s :%(message)s")
    if log_file_path is not None:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        handler = TimedRotatingFileHandler(filename=log_file_path, when="midnight", backupCount=backup_count, encoding="utf-8", delay=True)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    if std_out:
        handler = StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(log_level)
    logger.propagate = False
    return logger


def set_logger(name: str, log_conf: dict, backup_count: int = 180):
    """
    set the logger for different usage
    :param name:
    :param log_conf:
    :param backup_count:
    :return:
    """
    return get_common_logger(name, log_level=log_conf["level"],
                             log_file_path=os.path.dirname(__file__) + "/../.." + log_conf["log_file_path"],
                             std_out=log_conf["std_out"], backup_count=backup_count)
