import xml.dom.minidom
import os
import shutil
import math
from random import random


def read_xml(in_path) -> xml.dom.minidom.Document:
    """
    读取并解析xml文件
    :param in_path: xml路径
    :return: ElementTree
    """
    try:
        dom = xml.dom.minidom.parse(in_path)
        return dom
    except:
        print("XML file path %s error.\n" % in_path)


def write_xml(path, dom):
    '''
    xml存储函数
    :param path:存储路径
    :param dom:描述xml的dom对象
    :return:no return
    '''
    try:
        with open(path, 'w', encoding='UTF-8') as fh:
            dom.writexml(fh)
    except:
        print("Dom write error.")


def copy_file(srcfile, target_path):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        file_path, file_name = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(target_path):
            os.makedirs(target_path)  # 创建路径
        shutil.copy(srcfile, target_path + file_name)  # 复制文件
        print("copy %s -> %s" % (srcfile, target_path + file_name))


def shatter_number(upper, length):
    """
    将一个数撕裂为一个设定长度的随机数组
    :param upper:要被撕裂的数
    :param length:设定被撕裂的长度
    :return:r被撕裂的随机数列表，sum(r)随机数列表和
    """
    r = []
    for i in range(length):
        r.append(random())
    a_s = upper / sum(r)
    for i in range(len(r)):
        r[i] *= a_s
    return r, sum(r)


def my_softMax(num_list):
    num_list_exp = [math.exp(i) for i in num_list]
    sum_num_list_exp = sum(num_list_exp)
    return [round(i / sum_num_list_exp, 3) for i in num_list_exp]





def object2dict(obj):
    # convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


def dict2object(d):
    # convert dict to object
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key, value) for key, value in d.items())  # get args
        inst = class_(**args)  # create new instance
    else:
        inst = d
    return inst


def get_empty_dict(the_dict: dict):
    a_dict = {}
    for k, v in zip(the_dict.keys(), the_dict.values()):
        if v.__class__ != dict:
            a_dict[k] = v.__class__()
        else:
            a_dict[k] = get_empty_dict(v)
    return a_dict


def dict_to_xml_str(the_dict):
    """
    将字典转化为xml字符串
    :param the_dict:
    :return:
    """
    the_str = ""
    for k, v in the_dict.items():
        if v.__class__ != list:
            the_str += "<%s>""%s""</%s>" % (k, v, k) if not isinstance(v, dict) else "<%s>""%s""</%s>" % (
                k, dict_to_xml_str(v), k)
        else:
            for one_v in v:
                the_str += "<%s>""%s""</%s>" % (k, one_v, k) if not isinstance(one_v, dict) else "<%s>""%s""</%s>" % (
                    k, dict_to_xml_str(one_v), k)
    return the_str
