import sys
from math import pi, e


def global_attribute_1(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(pi, ele1, ele2, ele3)


def global_attribute_2(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(e, ele1, ele2, ele3)


def global_attribute_3(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(pi, ele1, ele2, ele3)

def global_attribute_4(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(pi, ele1, ele2, ele3)

def global_attribute_5(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(pi, ele1, ele2, ele3)

def global_attribute_6(ele1, ele2, ele3):
    print("in global attribute method", sys._getframe().f_code.co_name)
    print(pi, ele1, ele2, ele3)