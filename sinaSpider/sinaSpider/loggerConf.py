# -*- coding:utf-8 -*-
__author__ = 'xwk'
import logging
import logging.config

logging.config.fileConfig("logger/logger.conf")    # 采用配置文件

# create logger
logger = logging.getLogger("simpleLogger")

if __name__ == "__main__":
    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
