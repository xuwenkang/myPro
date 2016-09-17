# -*- coding:utf-8 -*-
__author__ = 'xwk'

import logging
import sinaSpider.loggerConf
from scrapy import cmdline

# 开始日志记录
logger = logging.getLogger('simpleLogger')
aim = 'scrapy crawl sinaSpider'
logger.debug('项目开始：')

# 项目执行
cmdline.execute(aim.split())


