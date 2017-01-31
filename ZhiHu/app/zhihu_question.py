# -*- coding:UTF-8 -*-
__author__ = 'xwk'
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET      # 不安全

from dataBase.xml_store import Converter
from theme_obj import Question

url = '/topic/19550994'
login_url = 'https://www.zhihu.com/#signin'
q_urls = 'https://www.zhihu.com/topic/19575492'

class QuestionCrawler():
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        # 并且进行登录
        # self.login()
    # 模拟登录
    def login(self):
        self.driver.get(login_url)
        # 通过用户名密码登录
        from settings import account, password
        self.driver.find_element_by_name('account').send_keys(account)
        self.driver.find_element_by_name('password').send_keys(password)
        # 点击登录按钮
        self.driver.find_element_by_class_name('submit').click()
        # 获取cookie 信息
        cookie = self.driver.get_cookies()
        print cookie

    # 获取问题列表
    def get_question_list(self):
        self.driver.get(q_urls)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        questions = soup.find_all('div', {'class': 'feed-content'})
        q_lists = []
        for question in questions:
            q_id = question.h2.a.get('data-id')
            q_url = question.h2.a.get('href')
            q_title = question.h2.get_text().strip()
            q_lists.append(Question(q_id, q_url, q_title))
        self.save_questions(q_lists)

    # 保存问题信息
    def save_questions(self, q_lists):
        # 判断文件是否存在
        if os.path.isfile('../xmlFile/questions.xml'):
            tree = ET.parse('../xmlFile/questions.xml')
            temp_root = tree.getroot()
            root = Converter.collection_to_xml(q_lists, temp_root)
        else:
            root = Converter.collection_to_xml(q_lists)
        # root = Converter.class_to_xml(theme)
        content = Converter.get_xml_string(root)
        with open('../xmlFile/questions.xml', 'ab') as f:
            f.write(content)

if __name__ == '__main__':
    crawler = QuestionCrawler()
    crawler.get_question_list()

