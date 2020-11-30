import xml.dom.minidom

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
    the_str = ""
    for k, v in the_dict.items():
        if v.__class__!=list:
            the_str += "<%s>""%s""</%s>" % (k, v, k) if not isinstance(v, dict) else "<%s>""%s""</%s>" % (
            k, dict_to_xml_str(v), k)
        else:
            for one_v in v:
                the_str+="<%s>""%s""</%s>" % (k, one_v, k) if not isinstance(one_v, dict) else "<%s>""%s""</%s>" % (
            k, dict_to_xml_str(one_v), k)
    return the_str