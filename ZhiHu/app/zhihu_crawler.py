# -*- coding:UTF-8 -*-
__author__ = 'xwk'
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import xml.etree.ElementTree as ET      # 不安全

from dataBase.xml_store import Converter
from theme_obj import Theme


class ZhiHuCrawler():
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    # 获取页面
    def get_home_page(self):
        driver = self.driver
        driver.get('https://www.zhihu.com/topics#生物学')
        #i = 1
        while True:
            #print i
            #i += 1
            time.sleep(1)
            #print driver.find_element_by_css_selector("a[aria-role=\"button\"]")
            try:
                elem = driver.find_element_by_css_selector("a[aria-role=\"button\"]")
            except:
                break
            elem.click()
        self.get_themes(driver.page_source)
        #soup.find_all('a', {'class': 'zg-btn-white zu-button-more'})

    # 获取所有的主题
    def get_themes(self, page_source):
        """
        :param page_source: selenium 获取的页面信息
        :return:
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        #items = soup.find_all('div', {'class': 'item'})
        items = soup.find_all('div', {'class': 'blk'})
        theme_list = []
        for item in items:
            # 获取主题不同的主题以及url
            theme_name = item.a.get_text().strip()
            theme_url = item.a.get('href')
            theme_list.append(Theme(theme_name, theme_url))
        self.save_info(theme_list)

    # 保存信息
    def save_info(self, theme):
        # 判断文件是否存在
        if os.path.isfile('../xmlFile/theme.xml'):
            tree = ET.parse('../xmlFile/theme.xml')
            temp_root = tree.getroot()
            root = Converter.collection_to_xml(theme, temp_root)
        else:
            root = Converter.collection_to_xml(theme)
        # root = Converter.class_to_xml(theme)
        content = Converter.get_xml_string(root)
        with open('../xmlFile/theme.xml', 'ab') as f:
            f.write(content)

if __name__ == '__main__':
    crawler = ZhiHuCrawler()
    crawler.get_home_page()