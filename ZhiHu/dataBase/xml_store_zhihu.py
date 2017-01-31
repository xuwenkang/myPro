# -*- coding:UTF-8 -*-
__author__ = 'xwk'
import xml.etree.ElementTree as ET      # 不安全
import xml.dom.minidom as minidom
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Converter(object):
    '''
    实现Python对象与xml之间的相互转换
    '''
    root = None     # 根节点
    def __init__(self):
        pass
    @staticmethod
    def create_root(root_tag):
        '''
        创建根节点
        :param root_tag:
        :return:
        '''
        root = ET.Element(root_tag)
        return root

    # 保存评论信息
    @staticmethod
    def save_comments_xml(class_obj):
        '''
        根据传入的对象的实例，根据对象的属性生成节点
        :param class_obj: 对象的实例
        :param rootTag: 根节点名称
        :return:
        '''
        attrs = None    # 保存对象的属性集
        elelist = []    # 节点列表
        try:
            attrs = class_obj.__dict__.keys()   # 获取该对象的所有属性
        except:
            print '传入的对象非法，不能正确获取对象的属性'

        if attrs and len(attrs) > 0:
            for attr in attrs:
                attr_value = getattr(class_obj, attr)   # 属性值
                # 属性节点
                if type(attr_value) == list:
                    for temp in attr_value:
                        attrE = ET.Element('comment_person')
                        # attrE.text = unicode(temp[0], "utf-8")
                        attrE.text = temp[0]
                        # 加入节点列表
                        elelist.append(attrE)
                        attrE = ET.Element('comment_content')
                        # attrE.text = unicode(temp[1], "utf-8")
                        attrE.text = temp[1]
                        # 加入节点列表
                        elelist.append(attrE)
                else:
                    attrE = ET.Element(attr)
                    attrE.text = attr_value
                    # 加入节点列表
                    elelist.append(attrE)
        return elelist

    @staticmethod
    def class_to_xml(class_obj, root_tag = None):
        '''
        Python自定义模型类转换成xml,转换成功返回的是xml根节点
        :param class_obj:
        :param rootTag:
        :return:
        '''
        try:
            class_name = class_obj.__class__.__name__      # 类名
            if root_tag != None:
                root = Converter.create_root(root_tag)
                #root = root_tag
            else:
                root = Converter.create_root(class_name)
            elelist = Converter.save_comments_xml(class_obj)
            for ele in elelist:
                root.append(ele)
            return root
        except:
            print '转换出错，请检查传入的对象是否正确'
            return None

    @staticmethod
    def get_xml_string(element, default_encoding='utf-8'):
        '''
        根据节点返回格式化的xml字符串
        :param element:
        :param default_encoding:
        :return:
        '''
        try:
            # rough_string = ET.tostring(element, encoding=default_encoding, method="xml")
            rough_string = ET.tostring(element, encoding=default_encoding, method="xml")
            print 'sb'
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent=" ", encoding=default_encoding)
        except:
            print 'get_xml_string：传入的节点不能正确转换为xml，检查传入的节点数据是否正确'
            return ''

class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
if __name__ == '__main__':
    p1 = Person('xwk', [('马伟涛', '有一次在屠宰厂看到一头牛，头和四肢都被切，内脏也没有，肌肉竟然还不停地抽动。'), ('male', 'female')])
    #tree = ET.parse('1.xml')
    #temp_root = tree.getroot()
    root = Converter.class_to_xml(p1)
    content = Converter.get_xml_string(root)
    print content