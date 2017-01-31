# -*- coding:UTF-8 -*-
__author__ = 'xwk'
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET      # 不安全
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

single_url = 'https://www.zhihu.com/question/54561783'

class SingleQuestionCrawler():
    def __init__(self, q_title, q_url, q_id):
        self.driver = webdriver.PhantomJS()
        self.q_title = q_title
        self.q_url = q_url
        self.q_id = q_id
        # 并且进行登录
        # self.login()
    # 获取问题信息
    def get_single_question(self, single_url):
        self.driver.get(single_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # print soup
        # 问题标签
        tags = ""
        contents = soup.find_all('a', {'class': 'zm-item-tag'})
        for content in contents:
            tags += content.get_text().strip()
            tags += '|'
        tags = tags[0:len(tags)-1]
        # 问题描述
        content = soup.find_all('div', {'class': 'zm-editable-content'})
        description = content[0].get_text().strip()
        # 评论数
        content = soup.find_all('a', {'name': 'addcomment'})
        comment_num = content[0].get_text().strip()
        # 回答
        contents = soup.find_all('h3', {'id': 'zh-question-answer-num'})
        answer_num = contents[0].get('data-num')
        # 获取评论列表
        comments = self.get_comment_list()  # 0 评论者；1 评论内容；2 评论者URL

        from theme_obj import Comment
        comments_list = []
        i = 1
        for temp_person, temp_content in zip(comments[0], comments[1]):
            """
            print i
            print temp_person.strip()
            print temp_content.strip()
            i += 1
            """
            comments_list.append((temp_person, temp_content))
        # 保存信息
        self.save_comments_info(Comment(self.q_id, self.q_url, self.q_title, tags, description, comments_list))

    # 获取评论列表
    def get_comment_list(self):
        # 评论信息列表（通过模拟点击，弹出 modal 框）
        elem = self.driver.find_element_by_name('addcomment')
        time.sleep(1)
        elem.click()
        # 加载时间很慢
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # 显示所有内容
        #elem1 = self.driver.find_element_by_name('load-more')
        elem1 = self.driver.find_element_by_class_name('load-more')
        print elem1
        elem1.click()
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        print soup
        contents = soup.find_all('div', {'class': 'zm-comment-hd'})
        # 获取评论者姓名
        comment_persons = []
        comment_persons_url = []
        for content in contents:
            try:
                t1 = content.span.get_text().strip()
                cc = content.span
                # 获取评论者url
                comment_persons_url.append(content.a.get('href').strip())
                if cc.next_sibling.next_sibling:
                    try:
                        t2 = cc.next_sibling.next_sibling.get_text().strip()
                        t3 = cc.next_sibling.next_sibling.next_sibling.get_text().strip()
                        comment_persons.append(t1 + t2 + t3)
                    except:
                        comment_persons.append('%s%s' % (t1.encode('utf-8'), ' 回复 知乎用户'))
                else:
                    comment_persons.append(t1)
                #t2 = content.a.next_sibling.next_sibling.strip()
                #t3 = content.a.next_sibling.next_sibling.next_sibling.next_sibling.strip()
            except:
                comment_persons.append(content.get_text().strip())
        # 获取评论内容
        comment_contents = []
        contents = soup.find_all('div', {'class': 'zm-comment-content'})
        for content in contents:
            comment_contents.append(content.get_text())
        # 返回元组
        return (comment_persons, comment_contents, comment_persons_url)

    # 保存评论信息
    def save_comments_info(self, comments):
        from dataBase.xml_store_zhihu import Converter
        # 判断文件是否存在
        if os.path.isfile('../xmlFile/comments.xml'):
            tree = ET.parse('../xmlFile/comments.xml')
            temp_root = tree.getroot()
            root = Converter.class_to_xml(comments, temp_root)
        else:
            root = Converter.class_to_xml(comments)
        # root = Converter.class_to_xml(theme)
        content = Converter.get_xml_string(root)
        print content
        with open('../xmlFile/comments.xml', 'ab') as f:
            f.write(content)


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
if __name__ == '__main__':
    crawler = SingleQuestionCrawler('有哪些很强大的事件或例子让人感觉，生命是如此强大？',
                                    '/question/54561783',
                                    '14044744')
    crawler.get_single_question(single_url)
    """
    from theme_obj import Comment
    comments_list = [('12', '12'), ('34', '34')]

    from dataBase.xml_store_zhihu import Converter
    root = Converter.class_to_xml(Comment('123', '123', '123', '123', '123', comments_list))
    print Converter.get_xml_string(root)
    """
    #ttt = ('1', [23, 4])
    #print ttt[1]