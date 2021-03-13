from other_tools import read_xml, write_xml
from external_file_for_cEvolution.create_task import dimension
from scipy import stats
from random import shuffle, randint
import numpy as np

member_dom = read_xml(r"ceMemberXml_C.xml")
primitive_labels = member_dom.getElementsByTagName("primitiveInfo")  # 原子型成员标签
shuffle(primitive_labels)
affector_labels = member_dom.getElementsByTagName("affectorInfo")  # 影响器标签
shuffle(affector_labels)
decider_labels = member_dom.getElementsByTagName("deciderInfo")  # 决策器标签
shuffle(decider_labels)
executor_labels = member_dom.getElementsByTagName("executorInfo")  # 执行器标签
shuffle(executor_labels)
connector_labels = member_dom.getElementsByTagName("connectorInfo")  # 联接器标签
shuffle(connector_labels)
name_list = ["决策器ID", "影响器ID", "执行器ID", "联接器ID", "监控器ID"]
for the_iter, the_labels in zip(name_list, [decider_labels, affector_labels, executor_labels, connector_labels]):
    for the_label, primitive_label in zip(the_labels, primitive_labels):
        primitive_label.setAttribute(the_iter, the_label.getAttribute(the_iter))

# 各种器安排完了,安排能够依照概率分布来设置属性值的属性
attribute_settings = [
    ("自律水平期望", "自律水平方差", "自律水平"),
    ("自信水平期望", "自信水平方差", "自信水平"),
    ("自退化率期望", "自退化率方差", "自退化率"),
    ("起始学习期望","起始学习方差","起始学习时间"),
    ("学习时间期望", "学习时间方差", "学习时间"),
    ("上限时间期望", "上限时间方差", "上限时间"),
]
primitive_comm_label = member_dom.getElementsByTagName("primitive")[0]
for expectation, variance, attr_name in attribute_settings:
    mu, sigma = float(primitive_comm_label.getAttribute(expectation)), float(
        primitive_comm_label.getAttribute(variance))
    lower, upper = mu - 4 * sigma, mu + 4 * sigma
    the_rvs = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    the_list = the_rvs.rvs(len(primitive_labels))
    for primitive_label, idx in zip(primitive_labels, range(len(the_list))):
        primitive_label.setAttribute(attr_name, str(the_list[idx]))

# 安排能力向量和学习率向量这一类向量变量
ability_matrix = np.zeros((dimension, len(primitive_labels)))
learn_matrix = np.zeros((dimension, len(primitive_labels)))
learn_mu_sigma_list = [(0.2, 0.07),
                       (0.3, 0.15),
                       (0.16, 0.06),
                       (0.29, 0.12),
                       (0.45, 0.12),
                       (0.34, 0.10),
                       (0.31, 0.12)]

ability_mu_sigma_list = [(0.17, 0.08),
                         (0.49, 0.2),
                         (0.72, 0.05),
                         (0.30, 0.12),
                         (0.35, 0.15),
                         (0.39, 0.12),
                         (0.48, 0.17)]
count = 0
for l_mu, l_sigma in learn_mu_sigma_list:
    l_lower, l_upper = l_mu - 2 * l_sigma, l_mu + 2 * l_sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((l_lower - l_mu) / l_sigma, (l_upper - l_mu) / l_sigma, loc=l_mu, scale=l_sigma)
    learn_matrix[count, :] = X.rvs(len(primitive_labels))
    count += 1
count = 0
for a_mu, a_sigma in ability_mu_sigma_list:
    a_lower, a_upper = a_mu - 2 * a_sigma, a_mu + 2 * a_sigma
    Y = stats.truncnorm((a_lower - a_mu) / a_sigma, (a_upper - a_mu) / a_sigma, loc=a_mu, scale=a_sigma)
    ability_matrix[count, :] = Y.rvs(len(primitive_labels))
    count += 1

for primitive_label, idx in zip(primitive_labels, range(len(primitive_labels))):
    primitive_label.setAttribute("能力向量", str(list(ability_matrix[:, idx])))
    primitive_label.setAttribute("学习向量", str(list(learn_matrix[:, idx])))
    primitive_label.setAttribute("外部学习向量", str([0 for _ in range(dimension)]))

# 安排格局上的初始点
# 获取格局初始点
init_position_list = []
position_labels = member_dom.getElementsByTagName("position")
for position_label in position_labels:
    position_type = position_label.getAttribute('type')
    if position_type == "start":
        init_position_list.append(position_label.getAttribute('pID'))

the_len=init_position_list.__len__()
for primitive_label in primitive_labels:
    if the_len==1:
        primitive_label.setAttribute("init_position", init_position_list[0])
        primitive_label.setAttribute("current_position", init_position_list[0])
    elif the_len>1:
        primitive_label.setAttribute("init_position", init_position_list[randint(0, the_len)])
    else:
        try:
            pass
        except ValueError:
            raise("pattern have no init position")

write_xml(r"ceMemberXml_C.xml", member_dom)
