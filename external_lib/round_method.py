import sys
import external_func
import members
from other_tools import read_xml


class Task(object):
    def __init__(self,task_label):
        self.task_id=task_label.getAttribute("ID")
        self.task_detail = eval(task_label.getAttribute("taskDetail"))
        self.start_time = None
        self.end_time = None
        self.executant = None


def p1(global_dict):
    # 读取任务
    task_dom = read_xml(r"E:\code\PycharmProjects\execution_tool\external_file\Task.xml")
    task_list=[]
    task_labels = task_dom.getElementsByTagName("task")
    for task_label in task_labels:
        a_task=Task(task_label)
        task_list.append(a_task)
    # 任务随机分配
    # 走众进化流程重新分配任务
    # 计算任务耗时
    # 计算各个成员能力向量的变化
    # 计算各个成员之间的连接关系变化
    print(global_dict['attr3'])

if __name__ == '__main__':
    p1({})