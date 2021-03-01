import members
import external_func
import numpy as np
import pattren
from other_tools import my_softMax


def adviser_method(global_dict, self_dict, primitive_dict, task):
    """
    :param global_dict:全局字典
    :param self_dict:调用本建议方法的建议者
    :param primitive_dict:寻求建议的primitive_dict
    :param task:需要给出建议的
    :return:
    """

    def task_pref_similar(task_detail, preference_vector):
        """
        计算相似程度
        :param task_detail: task的任务向量
        :param preference_vector: 建议者的偏好向量
        :return: '给自己' or '给别人'
        """
        my_softMax_vector = my_softMax(task_detail)
        X = [msv - pv for msv, pv in zip(my_softMax_vector, preference_vector)]
        return np.std(X) < self_dict['偏好阈值']
    # 获取比较结果
    res = task_pref_similar(task['task_detail'], self_dict['偏好向量'])
    # 获取当前该单元所在的位置ID
    current_position = primitive_dict['current_position']
    # 通过ID找到节点对象
    next_position_behavior = pattren.pattern_graph[current_position]
    # 此行代码看似毫无意义，实则遍历节点并对比计算是正确的选择
    for p, b in next_position_behavior.items():
        # 如果格局复杂，此处需要做计算确定p的返回
        if res == bool(int(next_position_behavior[p]['value'])):
            return res
        else:
            continue
    pass
