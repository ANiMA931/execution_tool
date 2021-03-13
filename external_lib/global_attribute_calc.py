import sys
import members


def latest_time_func(global_dict):
    the_latest_time = 0
    for p_dict in members.primitive_dict.values():
        if p_dict['耗时'] > the_latest_time:
            the_latest_time = p_dict['耗时']
    global_dict['latest_time'] = the_latest_time
    print("in global attribute method {},latest_time={}".format(sys._getframe().f_code.co_name,
                                                                global_dict['latest_time']))


def average_time_func(global_dict):
    sum_time = 0
    for p_dict in members.primitive_dict.values():
        sum_time += p_dict['耗时']
    the_average_time = sum_time / len(members.primitive_dict)
    global_dict['average_time'] = the_average_time
    print("in global attribute method {},average_time={}".format(sys._getframe().f_code.co_name,
                                                                 global_dict['average_time']))


def late_count_func(global_dict):
    """不能做的task的个数，在执行器中更改"""
    print(
        "in global attribute method {},late_count={}".format(sys._getframe().f_code.co_name, global_dict['late_count']))


def loss_func(global_dict):
    """损失总量，在执行器中更改"""
    print("in global attribute method {},loss={}".format(sys._getframe().f_code.co_name, global_dict['loss']))


def delay_count_func(global_dict):
    """延时个数，在执行器中更改"""
    print("in global attribute method {}, delay_count={}".format(sys._getframe().f_code.co_name,
                                                                 global_dict['delay_count']))


def delay_loss_func(global_dict):
    """延时损失，在执行器中更改"""
    print("in global attribute method {}, delay_loss={}".format(sys._getframe().f_code.co_name,
                                                                global_dict['delay_loss']))


def average_ability_func(global_dict):
    """平均能力向量"""
    sum_list = [0 for _ in range(members.primitive_dict['memberID-0']['能力向量'].__len__())]
    for p_dict in members.primitive_dict.values():
        ab_list = p_dict['能力向量']
        for i in range(len(sum_list)):
            sum_list[i] += ab_list[i]
    global_dict['average_ability'] = [i / len(members.primitive_dict) for i in sum_list]
    print("in global attribute method {}, average_ability=\n{}".format(sys._getframe().f_code.co_name,
                                                                       global_dict['average_ability']))


def benefits_func(global_dict):
    benefits=0
    for p_dict in members.primitive_dict.values():
        benefits += p_dict['收益总和']
    global_dict['benefits']=benefits
    print("in global attribute method {}, benefits={}".format(sys._getframe().f_code.co_name, global_dict['benefits']))
