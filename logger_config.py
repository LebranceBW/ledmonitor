import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, level=logging.INFO):
    """设置日志记录器，同时输出到文件和控制台"""
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    # 创建日志目录（如果不存在）
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 设置日志录器
logger = setup_logger("ledmonitor", "logs/ledmonitor.log")
