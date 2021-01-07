import sys
import external_func
import members
from other_tools import read_xml


class Task(object):
    def __init__(self, task_label):
        self.task_id = task_label.getAttribute("ID")
        self.task_detail = eval(task_label.getAttribute("taskDetail"))
        self.start_time = None
        self.end_time = None
        self.executant = None


def p1(global_dict):
    # 读取任务
    task_dom = read_xml(r"E:\code\PycharmProjects\execution_tool\external_file\Task.xml")
    task_dict = {}
    task_labels = task_dom.getElementsByTagName("task")
    for task_label in task_labels:
        a_task = Task(task_label)
        task_dict.update({a_task.task_id: a_task})
    # 任务装配
    for a_primitive_dict in members.primitive_dict:
        true_id_list=[]
        for ti_id in a_primitive_dict['decider']['任务ID集合']:
            true_id_list.append(task_dict[ti_id])
        a_primitive_dict['decider']['任务ID集合']=true_id_list
    # 走众进化流程重新分配任务
    # 计算任务耗时dtrhthedthd
    # 计算各个成员能力向量的变化

    # 计算各个成员之间的连接关系变化

    print()


if __name__ == '__main__':
    p1({})
