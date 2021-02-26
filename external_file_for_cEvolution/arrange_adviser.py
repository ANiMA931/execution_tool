from other_tools import read_xml, write_xml
from external_file_for_cEvolution.create_task import dimension
from scipy import stats
from random import shuffle, random
import numpy as np

member_dom = read_xml(r"ceMemberXml_C.xml")
adviser_labels = member_dom.getElementsByTagName("adviserInfo")  # 原子型成员标签
shuffle(adviser_labels)

preference_matrix = np.zeros((dimension, len(adviser_labels)))
preference_mu_sigma_list = [(0.2, 0.07),
                            (0.3, 0.15),
                            (0.16, 0.06),
                            (0.59, 0.25),
                            (0.45, 0.12),
                            (0.54, 0.20),
                            (0.31, 0.12)]
count = 0
for l_mu, l_sigma in preference_mu_sigma_list:
    l_lower, l_upper = l_mu - 2 * l_sigma, l_mu + 2 * l_sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((l_lower - l_mu) / l_sigma, (l_upper - l_mu) / l_sigma, loc=l_mu, scale=l_sigma)
    preference_matrix[count, :] = X.rvs(len(adviser_labels))
    count += 1

for adviser_label, idx in zip(adviser_labels, range(len(adviser_labels))):
    adviser_label.setAttribute("偏好向量", str(list(preference_matrix[:, idx])))
    adviser_label.setAttribute("偏好阈值", str(random()))
write_xml(r"ceMemberXml_C.xml", member_dom)
