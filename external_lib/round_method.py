import sys
import external_func
import members
import pattren

from other_tools import read_xml,object2dict


class Task(object):
    def __init__(self, task_label):
        self.task_id = task_label.getAttribute("ID")
        self.task_detail = eval(task_label.getAttribute("taskDetail"))
        self.start_time = None
        self.end_time = None
        self.executant = None

task_dom = None
task_dict = None
task_labels = None

def p1(global_dict):
    # 读取任务
    for a_p_dict in members.primitive_dict.values():
        if a_p_dict['决策器']['任务ID集合'].__len__() != 0:
            global task_dom,task_dict,task_labels
            if a_p_dict['决策器']['任务ID集合'][0].__class__ is not dict:
                if task_dom is None:
                    task_dom = read_xml(r"external_file/Task.xml")
                    task_dict = {}
                    task_labels = task_dom.getElementsByTagName("task")
                for task_label in task_labels:
                    a_task = Task(task_label)
                    a_task_dict = object2dict(a_task)
                    task_dict.update({a_task.task_id: a_task_dict})
                # 任务装配
                for a_primitive_dict in members.primitive_dict.values():
                    true_id_list=[]
                    for ti_id in a_primitive_dict['决策器']['任务ID集合']:
                        true_id_list.append(task_dict[ti_id])
                    a_primitive_dict['决策器']['任务ID集合']=true_id_list
    # 走众进化流程重新分配任务
    print(global_dict['attr1'])
    # 计算任务耗时

    # 计算各个成员能力向量的变化

    # 计算各个成员之间的连接关系变化

    print(123456789)


if __name__ == '__main__':
    p1({'attr1':1})
