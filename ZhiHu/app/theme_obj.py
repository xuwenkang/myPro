# -*- coding:UTF-8 -*-
__author__ = 'xwk'

"""
    知乎主题
"""
class Theme:
    def __init__(self, theme_name, theme_url):
        self.name = theme_name
        self.url = theme_url
"""
    知乎问题
"""
class Question:
    def __init__(self, q_id, url, title, tags, description, comment_persons):
        self.q_id = q_id
        self.q_url = url
        self.q_title = title
        self.q_tags = tags
        self.q_description = description
        self.q_comment_persons = comment_persons
"""
    知乎评论
"""
class Comment:
    def __init__(self, q_id, url, title, tags, description, comments_list):
        self.q_id = q_id
        self.q_url = url
        self.q_title = title
        self.q_tags = tags
        self.q_description = description
        self.q_comments = comments_list