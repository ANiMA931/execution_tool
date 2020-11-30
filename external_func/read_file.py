import external_func
import xml.dom.minidom
import sys


def read_global_attribute(xml_dom: xml.dom.minidom.Document, global_dict: dict):
    """
    读取仿真定义文件中定义的全局属性递推方法
    :param xml_dom:
    :return:
    """
    global_attribute_method_labels = xml_dom.getElementsByTagName('GlobalAttributeRecursionMethod')
    global_func_msg = {}
    global_func_ptr = []
    for global_attribute_method_label in global_attribute_method_labels:
        global_func_msg.update({
            global_attribute_method_label.getAttribute('fName'): {
                'name': global_attribute_method_label.getAttribute('fName'),
                'ID': global_attribute_method_label.getAttribute('ID'),
                'attribute_type': {},
                'attributes': {},
                'aName': global_attribute_method_label.getAttribute('aName'),
                'val': eval(global_attribute_method_label.getAttribute('init')),
            }
        })
        # 这里直接调用globals()是没有用的，必须要用参数引进添加才可以
        global_dict.update({global_attribute_method_label.getAttribute('aName'): eval(
            global_attribute_method_label.getAttribute('init'))})
        for one_attribute_label in global_attribute_method_label.getElementsByTagName('attribute'):
            global_func_msg[global_attribute_method_label.getAttribute('fName')]['attribute_type'].update({
                one_attribute_label.getAttribute('name'): one_attribute_label.getAttribute('type'),
            })
            global_func_msg[global_attribute_method_label.getAttribute('fName')]['attributes'].update({
                one_attribute_label.getAttribute('name'): None,
            })
        if global_attribute_method_label.getAttribute('path') not in sys.path:
            sys.path.append(global_attribute_method_label.getAttribute('path'))
        global_attribute_calc = __import__('global_attribute_calc',
                                           fromlist=(global_attribute_method_label.getAttribute('fName'),))
        global_func_ptr.append(eval('global_attribute_calc.' + global_attribute_method_label.getAttribute('fName')))
    external_func.global_attribute_dict = global_func_msg
    external_func.global_attribute_func_ptrs = global_func_ptr
    external_func.old_global_attribute_dict = external_func.global_attribute_dict.copy()
    return global_func_ptr


def read_generation_method(xml_dom: xml.dom.minidom.Document):
    """
    读取仿真定义文件中定义的代方法推进办法
    :param xml_dom:
    :return:
    """
    inherited_label = xml_dom.getElementsByTagName('inherited')[0]
    if inherited_label.firstChild.data == '1':
        external_func.generation_method = True
    elif inherited_label.firstChild.data == '0':
        external_func.generation_method = False
    else:
        input("inherited_label: " + inherited_label.firstChild.data + " wrong")
        exit(1)


def read_round_method(xml_dom: xml.dom.minidom.Document):
    """
    读取仿真定义文件中定义的轮方法
    :param xml_dom:
    :return: 轮方法函数指针
    """
    round_method_label = xml_dom.getElementsByTagName('TheRoundMethod')[0]
    if round_method_label:
        external_func.round_method_dict = {
            'name': round_method_label.getAttribute('name'),
            'ID': round_method_label.getAttribute('ID'),
            'attribute_type': {},
            'attributes': {},
        }
    for one_attribute_label in round_method_label.getElementsByTagName('attribute'):
        external_func.round_method_dict['attribute_type'].update({
            one_attribute_label.getAttribute('name'): eval(one_attribute_label.getAttribute('type')),
        })
        external_func.round_method_dict['attributes'].update({
            one_attribute_label.getAttribute('name'): None,
        })
    if round_method_label.getAttribute('path') not in sys.path:
        sys.path.append(round_method_label.getAttribute('path'))
    the_round_method_module = __import__('round_method', fromlist=(external_func.round_method_dict['name'],))
    external_func.round_method = eval('the_round_method_module.' + external_func.round_method_dict['name'])
    return eval('the_round_method_module.' + external_func.round_method_dict['name'])


def read_round_number(xml_dom: xml.dom.minidom.Document):
    round_number_label = xml_dom.getElementsByTagName('simulationRoundNumber')[0]
    external_func.round_number = int(round_number_label.firstChild.data)
    return external_func.round_number


def read_xml_to_module(xml_dom: xml.dom.minidom.Document, global_dict: dict):
    read_round_number(xml_dom)
    read_round_method(xml_dom)
    read_global_attribute(xml_dom, global_dict)
    read_generation_method(xml_dom)
    external_func.round_number = int(xml_dom.getElementsByTagName('simulationRoundNumber')[0].firstChild.data)
    external_func.external_func_dom = xml_dom
