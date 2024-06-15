# logger_setup.py
import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

# ANSI escape codes for coloring output
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34m"
    white = "\x1b[37m"
    reset = "\x1b[0m"
    
    # 格式中的基本部分
    base_format = "%(asctime)s - %(levelname)s - "
    file_info_format = blue + "(%(filename)s:%(lineno)d)" + reset

    # 特定于日志级别的消息格式
    FORMATS = {
        logging.DEBUG: grey + base_format + grey + "%(message)s " + reset + file_info_format,
        logging.INFO: green + base_format + white + "%(message)s " + reset + file_info_format,
        logging.WARNING: yellow + base_format + yellow + "%(message)s " + reset + file_info_format,
        logging.ERROR: red + base_format + red + "%(message)s " + reset + file_info_format,
        logging.CRITICAL: bold_red + base_format + bold_red + "%(message)s " + reset + file_info_format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(log_directory="logs"):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 确定当前日期并设置初始文件名
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    initial_log_filename = os.path.join(log_directory, f"app-{today}.log")

    # 检查文件是否存在，如果不存在，创建一个带日期后缀的文件
    if not os.path.exists(initial_log_filename):
        open(initial_log_filename, 'a').close()

    # 配置日志文件和TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(initial_log_filename, when="midnight", interval=1)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'))

    # 配置日志器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # 添加颜色日志到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    return logger
