# -*- coding:utf-8 -*-
import logging
import os
import time
from logging import handlers


class Log(object):
    def __init__(self):
        logs_path = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        name_format = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self._log_name = f"{logs_path}/{name_format}.log"

    def set_logger(self):
        # 创建一个logger,可以考虑如何将它封装
        loggers = logging.getLogger(self._log_name)
        loggers.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件, 存 3 个日志，每个 10M 大小
        fh = handlers.RotatingFileHandler(self._log_name, maxBytes=10 * 1024 * 1024, backupCount=3,
                                          encoding="UTF-8")
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - '
                                      '%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        loggers.addHandler(fh)
        loggers.addHandler(ch)
        return loggers


logger = Log().set_logger()
