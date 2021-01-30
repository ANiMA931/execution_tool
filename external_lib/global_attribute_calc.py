import sys
import members

def global_attribute_1(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(members.primitive_dict['memberID-0']['自信水平'])
    global_dict['attr1']+=0.09

def global_attribute_2(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    global_dict['attr2']+=0.06


def global_attribute_3(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    global_dict['attr3']+=0.07

def global_attribute_4(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    global_dict['attr4']+=0.03

def global_attribute_5(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    global_dict['attr5']+=0.02

def global_attribute_6(global_dict):
    print("in global attribute method", sys._getframe().f_code.co_name)
    global_dict['attr6']+=0.1