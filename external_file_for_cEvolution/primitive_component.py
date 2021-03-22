import sys
import members
import external_func
import numpy as np
from random import random
from other_tools import my_softMax


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
    suggestion_result = {'False': 0, 'True': 0}
    for one_adv_id, strength in adv_items:
        res = members.adviser_method(global_dict, members.adviser_dict[one_adv_id], self_dict, task)
        if res in suggestion_result:
            suggestion_result[str(res)] += strength['strength']
        else:
            suggestion_result.update({str(res): strength['strength']})
    return suggestion_result


def decider_method(global_dict, self_dict, task, self_pri_dict):
    """
    决策器外部函数
    :param global_dict:全局字典
    :param self_dict:调用本决策的primitive_dict
    :param task:需要针对做出决策的task
    :param self_pri_dict:调用该决策器的成员连接着谁
    :return:一个primitive的id
    """

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
            # 此处是累加计算，时间相较于木桶原理更长
            sum_t += mission / ability
        return sum_t

    # 声明结果集
    the_id = self_dict['原子型成员ID']
    # 首先确定，哪些成员可以被推出来
    # 先获得所有的ID
    # 如果该ID已经存在于task的past_list的里面了，删掉该标签
    for task_past in task['past_list']:
        if task_past in self_pri_dict.keys():
            self_pri_dict.__delitem__(task_past)
    # 如果dict没空
    if self_pri_dict:
        # 获取当前的primitive相连的dict对象的耗时
        time_cost_dict = {}
        # 如果这个task不是被自己转送出去的，那么把自己也考虑今去
        if self_dict['原子型成员ID'] not in task['past_list']:
            time_cost_dict.update({self_dict['原子型成员ID']: self_dict['耗时']})
        # 如果被送回来了，假定只能自己做，所以是强宣称（此处被送回来的原因是上家发生了突变并监控失败了(此处通过逻辑规避）
        else:
            return the_id, True

        for pri_id in self_pri_dict.keys():
            cost_time = members.primitive_dict[pri_id]['耗时']
            time_cost_dict.update({pri_id: cost_time})

        # 耗时获取完毕之后，
        # 此处的策略是多重的，有谁做的最快交给谁做，有尽量使均匀分布的做法，
        # 找出一个能得到最小标准差的或者当前耗时最少的，下列代码是获得标准差最小的流程
        min_std = float('inf')
        for pri_id in time_cost_dict.keys():
            # 先获得一个复制品
            time_cost_dict_copy = time_cost_dict.copy()
            # 获得计算时间
            tmp_t = get_work_time(task, members.primitive_dict[pri_id])
            # 获得的计算
            time_cost_dict_copy[pri_id] += tmp_t
            # 计算标准差
            the_std = np.std(list(time_cost_dict_copy.values()))
            # 如果新的标准差更小
            if the_std < min_std:
                min_std = the_std
                the_id = pri_id
        # 说明本任务被本单元转手了，通过该方式获得的结果，都是弱宣称
        task['past_list'].append(self_dict['原子型成员ID'])
        return the_id, False
    # 如果空了，表示本task都被其他人转手过了，直接返回the_id，并赋予强宣称，表示无法突变
    else:
        return the_id, True


def executor_method(global_dict, self_dict, task):
    """
    执行器外部函数，需要将正在处理的task给放置到当前的primitive的任务列表中，并且取出计算时间
    :param global_dict:全局字典
    :param self_dict:调用本执行器的原子型成员字典
    :param task:需要处理的执行器
    :return:
    """

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
            # 此处是累加计算，时间相较于木桶原理更长
            sum_t += mission / ability
        return sum_t

    # 计算消耗的时间
    task['spend_time'] = get_work_time(task, self_dict)
    if self_dict['耗时'] + task['spend_time'] > self_dict['上限时间']:
        task['executant'] = "None"
        global_dict['loss'] -= task['earn']
        global_dict['late_count'] += 1
        return
    else:
        # 记录完成此任务的个体
        task['executant'] = self_dict['原子型成员ID']
        # 如果在时限内完成了
        if task['spend_time'] <= task['time_limit']:
            task['e_flag'] = True
            self_dict['收益总和'] += task['earn']
            CIQ_list = []
            for i in range(len(task['task_detail'])):
                if task['task_detail'][i] != 0:
                    CIQ_item = self_dict['能力向量'][i] * self_dict['质量向量'][i] / task['task_detail'][i]
                else:
                    CIQ_item = 0
                CIQ_list.append(CIQ_item)
            self_dict['CIQ'] += sum(CIQ_list)
        else:
            CIQ_list = []
            for i in range(len(task['task_detail'])):
                if task['task_detail'][i] != 0:
                    CIQ_item = self_dict['能力向量'][i] * self_dict['质量向量'][i] / task['task_detail'][i]
                else:
                    CIQ_item = 0
                CIQ_list.append(CIQ_item)
            self_dict['收益总和'] -= task['earn'] * 0.3
            global_dict['delay_loss'] += task['earn'] * 0.3
            global_dict['delay_count'] += 1
            self_dict['CIQ'] += sum(CIQ_list)
        self_dict['任务列表'].append(task)

        self_dict['耗时'] += task['spend_time']
        # 如果当前耗时没有超过学习时间，说明该任务可以被学习
        if self_dict['耗时'] < self_dict['学习时间']:
            self_dict['学习列表'].append(task)
        # 超过了学习时间，则学不动了，只能获取其收益了
        else:
            pass
        pass


def monitor_method(global_dict, self_dict, mon_items):
    """
    监控器外部函数，返回自身+外部的监督成功概率
    :param global_dict:全局字典
    :param self_dict:调用监控器的方法
    :return:返回是否监控成功
    """
    external_mon = False
    for mon_id, mon_dict in mon_items:
        external_mon = external_mon and members.monitorMember_method(global_dict, mon_dict, self_dict)
    return random() < self_dict['自律水平'] or external_mon


def connector_method(global_dict, self_dict):
    """
    连接器外部函数
    :param global_dict:
    :param self_dict:
    :return:
    """
    # 联接器负责调整关系权重，更新外部学习变量，该关系权重包含三大关系，原子型成员之间的关系，原子型成员与建议者们的关系，原子型成员与监控者们的关系
    # 原子型成员之间的关系
    p2p_net = members.network_dict['net-p2p']
    self_node = p2p_net[self_dict['原子型成员ID']]
    pri_rel_id_list = list(self_node._atlas.keys())
    difference_list = [0 for _ in range(len(pri_rel_id_list))]
    for idx, diff in enumerate(difference_list):
        for i in range(len(self_dict['能力向量'])):
            if members.primitive_dict[pri_rel_id_list[idx]]['能力向量'][i] > self_dict['能力向量'][i]:
                difference_list[idx] += members.primitive_dict[pri_rel_id_list[idx]]['能力向量'][i] - self_dict['能力向量'][i]
    rel_list = my_softMax(difference_list)
    for idx, id in enumerate(pri_rel_id_list):
        p2p_net[self_dict['原子型成员ID']][id]['strength'] = rel_list[idx]
    pass
