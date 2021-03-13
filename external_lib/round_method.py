import sys
import external_func
import members
import pattren
from random import random, shuffle


def task_recursion_traversal(global_dict, p_dict, task):
    """
    递归传递task
    :param global_dict:
    :param p_dict:
    :param task:
    :return:
    """
    # 获取本单元的局部网络
    p2a_net = members.network_dict['net-p2a']
    p2p_net = members.network_dict['net-p2p']
    p2m_net = members.network_dict['net-p2m']
    p2a_self_node = p2a_net[p_dict['原子型成员ID']]
    p2p_self_node = p2p_net[p_dict['原子型成员ID']]
    p2m_self_node = p2m_net[p_dict['原子型成员ID']]

    # 获取建议者对象列表
    self_adv_items = p2a_self_node._atlas.items()
    self_pri_items = p2p_self_node._atlas.items()
    self_mon_items = p2m_self_node._atlas.items()
    # 调用影响器
    sug_res_dict = members.primitive_components['affector_method'](
        global_dict, p_dict, self_adv_items, task
    )
    # 调用决策器，获得目标id与宣称
    to_id, allege = members.primitive_components['decider_method'](global_dict, p_dict, task,
                                                                   p2p_self_node._atlas.copy())
    sug_res_dict[str(to_id == p_dict['原子型成员ID'])] += p_dict['自信水平']
    pre_val, pre_action = 0, None
    for sug, val in sug_res_dict.items():
        if val > pre_val:
            pre_val = val
            pre_action = sug
    mutation_flag = random() < p_dict['执行器ID']['突变率']
    # 如果是自己做并且不是强宣称，说明存在其他单元没有转手过本task
    if eval(pre_action) and not allege:
        # 如果突变与则进入监控
        if mutation_flag:
            # 监控是否成功
            monitor_flag = members.primitive_components['monitor_method'](global_dict, p_dict, self_mon_items)
            # 监控成功
            if monitor_flag:
                # 执行器添加即可
                members.primitive_components['executor_method'](global_dict, p_dict, task)
            # 监控失败
            else:
                # 给出一个可行的随机选项，然后递归进入下一层
                past_id_list = task['past_list'].copy()
                pri_list = p2p_self_node._atlas.keys()
                valid_pri = list(set(pri_list) - set(past_id_list))
                shuffle(valid_pri)
                task_recursion_traversal(global_dict, members.primitive_dict[valid_pri[0]], task)
                pass
        # 未突变
        else:
            # 执行器添加即可
            members.primitive_components['executor_method'](global_dict, p_dict, task)
    # 如果是别人做，别人做都是弱宣称
    elif not eval(pre_action) and not allege:
        if mutation_flag:
            # 监控是否成功
            monitor_flag = members.primitive_components['monitor_method'](global_dict, p_dict, self_mon_items)
            # 如果成功
            if monitor_flag:
                # 递归操作
                task_recursion_traversal(global_dict, members.primitive_dict[to_id], task)
            else:
                # 给出一个可行的随机选项
                past_id_list = task['past_list'].copy()
                pri_list = p2p_self_node._atlas.keys()
                valid_pri = list(set(pri_list) - set(past_id_list))
                shuffle(valid_pri)
                # 如果是自己，给自己添加
                if valid_pri[0] == p_dict['原子型成员ID']:
                    members.primitive_components['executor_method'](global_dict, p_dict, task)
                # 如果是别人，新的递归操作
                else:
                    task_recursion_traversal(global_dict, members.primitive_dict[valid_pri[0]], task)
        # 未突变
        else:
            # 递归操作
            task_recursion_traversal(global_dict, members.primitive_dict[to_id], task)
    # 强宣称，必须自己做，不突变
    else:
        members.primitive_components['executor_method'](global_dict, p_dict, task)


def learn(global_dict, p_dict):
    """
    学习函数，是将所有的学习列表中的工作量相加，然后相应上升
    :param global_dict:
    :param p_dict:
    :return:
    """
    # 超过了一定的学习时间，学习才是有效的，否则直接退化
    if p_dict['耗时'] > p_dict['起始学习时间']:
        task_dimension = len(p_dict['能力向量'])
        tmp_task_sum_list = [0 for _ in range(task_dimension)]
        for learn_task in p_dict['学习列表']:
            for dim in range(task_dimension):
                tmp_task_sum_list[dim] += learn_task['task_detail'][dim]
        learn_rate_list = [0 for _ in range(task_dimension)]
        for dim in range(task_dimension):
            learn_rate_list[dim] = (p_dict['学习向量'][dim] + p_dict['外部学习向量'][dim]) / (1 + p_dict['外部学习向量'][dim])
        incremental = [tsl * rl for tsl, rl in zip(tmp_task_sum_list, learn_rate_list)]
        p_dict['能力向量'] = [(ab_part * 1000 + inc_part) / (1000 + inc_part) for ab_part, inc_part in
                          zip(p_dict['能力向量'], incremental)]


def cal_external_learn_vector(global_dict, p_dict):
    net_p2p = members.network_dict['net-p2p']
    self_node = net_p2p[p_dict['原子型成员ID']]
    pri_node_id_list = list(self_node._atlas.keys())
    for id in pri_node_id_list:
        external_influence = [i * net_p2p[p_dict['原子型成员ID']][id]['strength'] for i in
                              members.primitive_dict[id]['能力向量']]
        for idx, j in enumerate(external_influence):
            p_dict['外部学习向量'][idx] += j


def restore(global_dict, a_p_dict):
    """
    重置信息
    :param a_p_dict:
    :return:
    """
    a_p_dict['耗时'] = 0
    a_p_dict['收益总和'] = 0
    a_p_dict['决策器ID']['任务ID集合'] = a_p_dict['初始任务列表'].copy()
    a_p_dict['任务列表'].clear()
    a_p_dict['学习列表'].clear()
    a_p_dict['current_position'] = a_p_dict['init_position']
    global_dict['loss'] = 0
    global_dict['late_count'] = 0
    global_dict['delay_count'] = 0
    global_dict['delay_loss'] = 0


def p1(global_dict):
    for p_dict in members.primitive_dict.values():
        restore(global_dict, p_dict)
        # 从这一步开始，就要开始走流程了
    for p_dict in members.primitive_dict.values():
        tasks = p_dict['决策器ID']['任务ID集合']
        for task in tasks:
            # 这个地方要写递归
            task_recursion_traversal(global_dict, p_dict, task)
    # 计算退化
    for p_dict in members.primitive_dict.values():
        if p_dict['耗时'] < p_dict['起始学习时间']:
            p_dict['能力向量'] = [ab_part * (1 - p_dict['自退化率']) for ab_part in p_dict['能力向量']]
    # 计算各个成员的外部学习向量
    for p_dict in members.primitive_dict.values():
        cal_external_learn_vector(global_dict, p_dict)
    # 计算各个成员新的能力向量
    for p_dict in members.primitive_dict.values():
        learn(global_dict, p_dict)
    # 计算各个成员之间的连接关系变化
    for p_dict in members.primitive_dict.values():
        members.primitive_components['connector_method'](global_dict, p_dict)
    # 避免记录过多不必要的内容
    for p_dict in members.primitive_dict.values():
        p_dict['决策器ID']['任务ID集合'].clear()


if __name__ == '__main__':
    p1({'attr1': 1})
