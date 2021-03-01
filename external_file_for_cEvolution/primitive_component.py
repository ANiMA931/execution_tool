import sys
import members
import external_func


def affector_method(global_dict, self_dict, adv_items, task):
    """
    影响器函数
    :param global_dict:全局字典
    :param self_dict:调用该影响器的primitive_dict
    :param adv_items: 与调用该影响器的primitive_dict相连的adviser
    :param task:影响器需要处理的task
    :return:建议结果集
    """
    # 声明结果集
    suggestion_result = {}
    for one_adv_id, strength in adv_items:
        res = members.adviser_method(global_dict, members.adviser_dict[one_adv_id], self_dict, task)
        if res in suggestion_result:
            suggestion_result[res] += strength['strength']
        else:
            suggestion_result.update({res: strength['strength']})
    return suggestion_result


def decider_method(global_dict, self_dict, task):
    """
    决策器外部函数
    :param global_dict:全局字典
    :param self_dict:调用本决策的primitive_dict
    :param task:需要针对做出决策的task
    :return:一个primitive的id
    """

    pass


def executor_method(global_dict, self_dict):
    """
    执行器外部函数
    :param global_dict:
    :param self_dict:
    :return:
    """
    pass


def monitor_method(global_dict, self_dict):
    """
    监控器外部函数
    :param global_dict:
    :param self_dict:
    :return:
    """
    pass


def connector_method(global_dict, self_dict):
    """
    连接器外部函数
    :param global_dict:
    :param self_dict:
    :return:
    """
    pass
