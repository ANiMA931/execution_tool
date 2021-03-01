import sys
import external_func
import members
import pattren

from random import random


def task_recursion_traversal(global_dict, p_dict, task):
    """
    递归传递task
    :param global_dict:
    :param p_dict:
    :param task:
    :return:
    """
    # 调用影响器
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
    sug_res_dict = members.primitive_components['affector_method'](
        global_dict, p_dict, task, self_adv_items
    )
    # 调用决策器
    to_id = members.primitive_components['decider_method'](global_dict, p_dict, self_pri_items)
    if to_id == p_dict['原子型成员ID']:
        sug_res_dict[True] += p_dict['自信水平']
    else:
        sug_res_dict[False] += p_dict['自信水平']
    pre_action = max(sug_res_dict)
    mutation_flag = p_dict['突变率'] < random()
    # 如果是自己做
    if pre_action:
        # 如果突变与则进入监控
        if mutation_flag:
            # 监控是否成功
            monitor_flag = members.primitive_components['monitor_method'](global_dict, p_dict, self_mon_items)
            # 监控成功
            if monitor_flag:
                # 执行器添加即可
                pass
            #监控失败
            else:
                # 给出一个随机选项，然后递归进入下一层
                pass
        # 未突变
        else:
            # 执行器添加即可
            pre_action =()
    # 如果是别人做
    else:
        if mutation_flag:
            # 监控是否成功
            monitor_flag = members.primitive_components['monitor_method'](global_dict, p_dict, self_mon_items)
            # 如果成功
            if monitor_flag:
                #递归操作
                pass
            else:
                # 给出一个随即选项
                # 如果是自己，给自己添加
                # 如果是别人，新的递归操作
                pass
        # 未突变
        else:
            # 递归操作
            pre_action =()


def task_traversal(p_dict):
    p2p_net = members.network_dict['net-p2p']

    def get_work_time(task, pri_dict):
        """
        计算一个task需要花多少时间才能做完
        :param task: task本体
        :return: 花费的时间
        """
        sum_t = 0
        task_detail_list = task['task_detail']
        p_ability = pri_dict['能力向量']
        for mission, ability in zip(task_detail_list, p_ability):
            sum_t += mission / ability
        return sum_t

    task_list = p_dict['决策器ID']['任务ID集合']

    for idx, one_task in enumerate(task_list):
        # 对每一个task进行递归式的任务分配
        # 计算本体处理该task的时间
        time = get_work_time(one_task, p_dict)
        min_time = time
        target = p_dict

        # 计算与本体相连的其他的p_dict的时间
        the_node = p2p_net[p_dict['原子型成员ID']]
        next_p_list = the_node._atlas.keys()
        next_p_list = list(set(next_p_list) - set(task_list[idx]['past_list']))
        for next_p in next_p_list:
            if next_p not in task_list[idx]['past_list']:
                time = get_work_time(one_task, members.primitive_dict[next_p])
                if time < min_time:
                    min_time = time
                    target = members.primitive_dict[next_p]
                    task_list[idx]['past_list'].append(target['原子型成员ID'])

        # 得到了与本单元连接的单元谁完成地最短
        if target['原子型成员ID'] == p_dict['原子型成员ID']:
            p_dict['任务列表'].append(one_task)
        else:
            task_list[idx]['past_list'].remove(target['原子型成员ID'])
            if task_list[idx] not in target['决策器ID']['任务ID集合']:
                target['决策器ID']['任务ID集合'].append(task_list[idx])
    task_list.clear()
    pass


def restore(a_p_dict):
    a_p_dict['耗时'] = 0
    a_p_dict['收益总和'] = 0
    a_p_dict['决策器ID']['任务ID集合'] = a_p_dict['初始任务列表'].copy()
    a_p_dict['任务列表'].clear()
    a_p_dict['current_position'] = a_p_dict['init_position']


def p1(global_dict):
    for p_dict in members.primitive_dict.values():
        restore(p_dict)
        # 从这一步开始，就要开始走流程了
    for p_dict in members.primitive_dict.values():
        tasks = p_dict['决策器ID']['任务ID集合']
        for task in tasks:
            # 这个地方要写递归
            task_traversal(p_dict)
            # 从影响器，到决策器，再到执行器，一旦定下来是某一个primitive，就切实得给到
            pass
        task_traversal(p_dict)
    # 计算任务耗时

    # 计算各个成员能力向量的变化

    # 计算各个成员之间的连接关系变化

    # 还原应还原的信息

    print(123456789)


if __name__ == '__main__':
    p1({'attr1': 1})
