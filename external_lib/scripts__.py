import members

from other_tools import read_xml, object2dict
from random import random


def p1(global_dict):
    print(members.primitive_dict['memberID-0'])


def p2(global_dict):
    global_dict['attr4'] = 954.49


def p3(global_dict):
    members.primitive_dict['memberID-1']['个人自信水平'] = 1.0


def evolution_init(global_dict):
    print(members.primitive_dict['memberID-0'])
    task_dom = read_xml(r"external_file_for_cEvolution/Task.xml")
    task_labels = task_dom.getElementsByTagName("task")
    task_dict = {}
    class Task(object):
        def __init__(self, task_label):
            self.task_id = task_label.getAttribute("ID")
            self.task_detail = eval(task_label.getAttribute("taskDetail"))
            self.time_limit = float(task_label.getAttribute("time_limit"))
            self.spend_time = None
            self.earn = float(task_label.getAttribute("earn"))
            self.executant = None
            self.e_flag = False
            self.past_list = []

    for a_p_dict in members.primitive_dict.values():
        a_p_dict.update({'任务列表':[]})
        a_p_dict.update({'学习列表':[]})
        a_p_dict.update({'耗时': 0})
        a_p_dict.update({'CIQ': 0})
        a_p_dict.update({'自退化率': random()})
        a_p_dict.update({'收益总和': 0})
        if a_p_dict['决策器ID'].__class__ is not str and a_p_dict['决策器ID']['任务ID集合'].__len__() != 0:
            if a_p_dict['决策器ID']['任务ID集合'][0].__class__ is not dict:
                for task_label in task_labels:
                    a_task = Task(task_label)
                    a_task_dict = object2dict(a_task)
                    task_dict.update({a_task.task_id: a_task_dict})
        # 任务装配
    for a_p_dict in members.primitive_dict.values():
        true_id_list=[]
        for ti_id in a_p_dict['决策器ID']['任务ID集合']:
            true_id_list.append(task_dict[ti_id])
        a_p_dict['决策器ID']['任务ID集合']=true_id_list
        a_p_dict.update({'初始任务列表': true_id_list.copy()})