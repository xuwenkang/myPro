# -*- coding:utf-8 -*-
__author__ = 'xwk'
import json
import codecs

class FilePipelines(object):
    def __init__(self):
        self.file = codecs.open('item1.txt', 'a', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        #line = dict(item)
        self.file.write(line.decode("unicode_escape"))
        return item
