# -*- coding:utf-8 -*-
__author__ = 'xwk'
import json
import codecs
from sinaSpider.items import InformationItem, TweetsItem, FollowsItem, FansItem


# 将爬取文件保存到文件中
class FilePipelines(object):
    def __init__(self):
        self.file = codecs.open('item1.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            file1 = codecs.open('pipeItem/information.txt', 'a', encoding='utf-8')
            line = json.dumps(dict(item)) + "\n"
            file1.write(line.decode("unicode_escape"))
        elif isinstance(item, TweetsItem):
            file1 = codecs.open('pipeItem/tweets.txt', 'a', encoding='utf-8')
            line = json.dumps(dict(item)) + "\n"
            file1.write(line.decode("unicode_escape"))
        elif isinstance(item, FollowsItem):
            file1 = codecs.open('pipeItem/follows.txt', 'a', encoding='utf-8')
            line = json.dumps(dict(item)) + "\n"
            file1.write(line.decode("unicode_escape"))
        elif isinstance(item, FansItem):
            file1 = codecs.open('pipeItem/fans.txt', 'a', encoding='utf-8')
            line = json.dumps(dict(item)) + "\n"
            file1.write(line.decode("unicode_escape"))
        #line = dict(item)
        #self.file.write(line.decode("unicode_escape"))
        return item






