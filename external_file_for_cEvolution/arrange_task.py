from other_tools import read_xml, write_xml
from random import shuffle, randint

member_dom = read_xml(r"ceMemberXml_C.xml")
task_dom = read_xml(r"Task.xml")
task_labels = task_dom.getElementsByTagName("task")
decider_labels = member_dom.getElementsByTagName("deciderInfo")
task_id_list = []
# 取出所有任务ID
for task_label in task_labels:
    task_id = task_label.getAttribute("ID")
    task_id_list.append(task_id)

# 集合划分
shuffle(task_id_list)
# 插板
tmp_indx = list(range(task_id_list.__len__() - 1))
index_ = []
for _ in range(len(decider_labels) - 1):
    shuffle(tmp_indx)
    index_.append(tmp_indx.pop(0))
index_.append(task_id_list.__len__() - 1)
index_.sort()
the_i = 0
# 取出所有原子型成员的决策器

for decider_label, k in zip(decider_labels, range(len(index_))):
    the_j = index_[k]
    decider_label.setAttribute("任务ID集合", str(task_id_list[the_i:the_j]))
    the_i = the_j

write_xml(r"ceMemberXml_C.xml", member_dom)
