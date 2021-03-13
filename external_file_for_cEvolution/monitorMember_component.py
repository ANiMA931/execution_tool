import members
import external_func
from random import random


def monitorMember_method(global_dict, self_dict, primitive_dict):
    """
    监控者的外部函数
    :param global_dict:
    :param self_dict:
    :param primitive_dict:
    :return:
    """
    edge = members.network_dict['net-p2m'][primitive_dict['原子型成员ID']][self_dict['监控者ID']]
    return random() < self_dict['监控强度'] * edge['strength']
