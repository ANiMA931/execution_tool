from other_tools import read_xml, write_xml, shatter_number
from itertools import permutations, product
from random import shuffle, seed,random


dom = read_xml(r"ceMemberXml_C.xml")
# 设置p2p-net
p_id_list = []
p_conn_id_list = []
p_labels = dom.getElementsByTagName("primitiveInfo")
p_conn_num_list = [0] * len(p_labels)
# 获得所有原子性单元的id
for p_label in p_labels:
    p_id_list.append(p_label.getAttribute("原子型成员ID"))
    p_conn_id_list.append(p_label.getAttribute("联接器ID"))

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
connet_label = dom.getElementsByTagName("connect")[0]
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
# 设置p2a-net
a_labels = dom.getElementsByTagName("adviserInfo")
adv_id_list = []
for a_label in a_labels:
    adv_id_list.append(a_label.getAttribute("建议者ID"))
rel_p_a = list(product(p_id_list, adv_id_list))
shuffle(rel_p_a)
rel_p_a = rel_p_a[:len(rel_p_a)//4]
p2a_net_label = dom.createElement("networkStructure")
p2a_net_label.setAttribute("ID","net-p2a")
p2a_net_label.setAttribute("type","p2a")
for arc in rel_p_a:
    conn_info_label = dom.createElement("connectInfo")
    conn_info_label.setAttribute("from",arc[0])
    conn_info_label.setAttribute("to", arc[1])
    conn_info_label.setAttribute("strength", str(random()))
    p2a_net_label.appendChild(conn_info_label)
connet_label.appendChild(p2a_net_label)


# 设置p2m-net
m_labels= dom.getElementsByTagName("monitorMemberInfo")
mon_id_list = []
for m_label in m_labels:
    mon_id_list.append(m_label.getAttribute("监控者ID"))
    m_label.setAttribute("监控强度", str(random()))
rel_p_m = list(product(p_id_list,mon_id_list))
shuffle(rel_p_m)
rel_p_m = rel_p_m[:len(rel_p_m)//4]
p2m_net_label = dom.createElement("networkStructure")
p2m_net_label.setAttribute("ID","net-p2m")
p2m_net_label.setAttribute("type","p2m")
for arc in rel_p_m:
    conn_info_label = dom.createElement("connectInfo")
    conn_info_label.setAttribute("from",arc[0])
    conn_info_label.setAttribute("to", arc[1])
    conn_info_label.setAttribute("strength", str(random()))
    p2m_net_label.appendChild(conn_info_label)
connet_label.appendChild(p2m_net_label)


write_xml("ceMemberXml_C.xml", dom)
