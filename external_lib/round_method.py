import sys
import external_func
import members
import pattren


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


def p1(global_dict):
    for p_dict in members.primitive_dict.values():
        restore(p_dict)
        # 从这一步开始，就要开始走流程了
    for p_dict in members.primitive_dict.values():
        tasks = p_dict['决策器ID']['任务ID集合']
        for task in tasks:
            # 这个地方要写递归
            # 从影响器，到决策器，再到执行器，再到算时间和
            pass
        task_traversal(p_dict)
    # 计算任务耗时

    # 计算各个成员能力向量的变化

    # 计算各个成员之间的连接关系变化

    # 还原应还原的信息

    print(123456789)


if __name__ == '__main__':
    p1({'attr1': 1})
