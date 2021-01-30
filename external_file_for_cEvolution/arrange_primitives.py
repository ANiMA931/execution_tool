from other_tools import read_xml, write_xml
from external_file_for_cEvolution.create_task import dimension
from scipy import stats
from random import shuffle
import numpy as np

member_dom = read_xml(r"E:\code\PycharmProjects\execution_tool\external_file\ceMemberXml_C.xml")
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
name_list = ["决策器ID", "影响器ID", "执行器ID", "联接器ID"]
for the_iter, the_labels in zip(name_list, [decider_labels, affector_labels, executor_labels, connector_labels]):
    for the_label, primitive_label in zip(the_labels, primitive_labels):
        primitive_label.setAttribute(the_iter, the_label.getAttribute(the_iter))
# 各种器安排完了,安排自律和自信
primitive_comm_label = member_dom.getElementsByTagName("primitive")[0]
sd_mu, sd_sigma = float(primitive_comm_label.getAttribute("自律水平期望")), float(primitive_comm_label.getAttribute("自律水平方差"))
sc_mu, sc_sigma = float(primitive_comm_label.getAttribute("自信水平期望")), float(primitive_comm_label.getAttribute("自信水平方差"))
sd_lower, sd_upper = sd_mu - 4 * sd_sigma, sd_mu + 4 * sd_sigma
sc_lower, sc_upper = sc_mu - 4 * sc_sigma, sc_mu + 4 * sc_sigma
SD = stats.truncnorm((sd_lower - sd_mu) / sd_sigma, (sd_upper - sd_mu) / sd_sigma, loc=sd_mu, scale=sd_sigma)
SC = stats.truncnorm((sc_lower - sc_mu) / sc_sigma, (sc_upper - sc_mu) / sc_sigma, loc=sc_mu, scale=sc_sigma)
sd_list = SD.rvs(len(primitive_labels))
sc_list = SC.rvs(len(primitive_labels))
for primitive_label, idx in zip(primitive_labels, range(len(sd_list))):
    primitive_label.setAttribute("自信水平", str(sc_list[idx]))
    primitive_label.setAttribute("自律水平", str(sd_list[idx]))
# 安排能力向量和学习率向量
ability_matrix = np.zeros((dimension, len(primitive_labels)))
learn_matrix = np.zeros((dimension, len(primitive_labels)))
learn_mu_sigma_list = [(0.2, 0.07),
                       (0.3, 0.15),
                       (0.16, 0.06),
                       (0.59, 0.25),
                       (0.45, 0.12),
                       (0.54, 0.20),
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
    ability_matrix[count, :]=Y.rvs(len(primitive_labels))
    count += 1

for primitive_label, idx in zip(primitive_labels, range(len(primitive_labels))):
    primitive_label.setAttribute("能力向量", str(list(ability_matrix[:,idx])))
    primitive_label.setAttribute("学习率向量", str(list(learn_matrix[:,idx])))
write_xml(r"E:\code\PycharmProjects\execution_tool\external_file\ceMemberXml_C.xml", member_dom)
