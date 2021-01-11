from other_tools import read_xml, write_xml, shatter_number
from itertools import permutations
from random import shuffle, seed

seed(9527)

dom = read_xml(r"D:\execution_tool\external_file\ceMemberXml_C.xml")
p_id_list = []
p_conn_id_list = []
p_labels = dom.getElementsByTagName("primitiveInfo")
p_conn_num_list = [0] * len(p_labels)
# 获得所有原子性单元的id
for p_label in p_labels:
    p_id_list.append(p_label.getAttribute("原子型成员ID"))
    p_conn_id_list.append(p_label.getAttribute("联接器"))

conn_labels = dom.getElementsByTagName("connectorInfo")
# 获得所有原子性单元的连接强度总和, 连接数量
for conn_label in conn_labels:
    tmp_weight = float(conn_label.getAttribute("平均连接强度"))
    tmp_num = int(conn_label.getAttribute("连接成员数量"))
    tmp_id = conn_label.getAttribute("联接器ID")
    t_idx = p_conn_id_list.index(tmp_id)
    p_conn_id_list[t_idx] = tmp_weight
    p_conn_num_list[t_idx] = tmp_num
# 生成一个connect_list
conn_relationship = []
conn_relationship_iter = permutations(p_id_list, 2)
for one_conn_relationship_iter in conn_relationship_iter:
    conn_relationship.append(list(one_conn_relationship_iter))
conn_dict = {}
# 获得保存网络关系的标签
net_labels = dom.getElementsByTagName("networkStructure")
p2p_net_label = None
for net_label in net_labels:
    if net_label.getAttribute("ID") == "net-p2p":
        p2p_net_label = net_label
    else:
        continue
for i, one_p in enumerate(p_id_list):
    tmp_list = conn_relationship[0:len(p_labels) - 1]
    conn_relationship = conn_relationship[len(p_labels) - 1:-1]
    shuffle(tmp_list)
    tmp_list = tmp_list[:p_conn_num_list[i]]
    weight_list, weight_sum = shatter_number(p_conn_id_list[i], p_conn_num_list[i])
    for weight, arc in zip(weight_list, tmp_list):
        arc.append(weight)
        conn_info_label = dom.createElement("connectInfo")
        conn_info_label.setAttribute("from", arc[0])
        conn_info_label.setAttribute("to", arc[1])
        conn_info_label.setAttribute("strength", str(arc[2]))
        p2p_net_label.appendChild(conn_info_label)
print()
write_xml("D:\execution_tool\external_file\ceMemberXml_C.xml",dom)
