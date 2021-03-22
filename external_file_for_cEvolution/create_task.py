import numpy as np
from other_tools import read_xml, write_xml
import scipy.stats as stats
import os

my_file = 'Task.xml'  # 文件路径
if os.path.exists(my_file):  # 如果文件存在
    # 删除文件，可使用以下两种方法。
    os.remove(my_file)  # 则删除
    # os.unlink(my_file)
else:
    print('no such file:%s' % my_file)

dimension = 7  # 7个维度
task_num = 200  # 200个基础task

mu_sigma_list = [
    (50, 15.9),
    (30, 3.9),
    (49, 6.7),
    (63, 12.5),
    (13, 6.1),
    (54, 20.6),
    (31, 12.2)
]

task_matrix = np.zeros([dimension, task_num])
count = 0
for the_mu, the_sigma in mu_sigma_list:
    lower, upper = the_mu - 2 * the_sigma, the_mu + 2 * the_sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((lower - the_mu) / the_sigma, (upper - the_mu) / the_sigma, loc=the_mu, scale=the_sigma)
    task_matrix[count, :] = X.rvs(task_num)
    count += 1

earn_list = []
time_list = []
attr_mu_sigma_list = [
    [60, 10, 'earn_list'],
    [600,100,'time_list']
]

for earn_mu, earn_sigma, i in attr_mu_sigma_list:
    l, u = earn_mu - 2 * earn_sigma, earn_mu + 2 * earn_sigma
    E = stats.truncnorm((l - earn_mu) / earn_sigma, (u - earn_mu) / earn_sigma, loc=earn_mu, scale=earn_sigma)
    the_list = eval(i)
    for j in list(E.rvs(task_num)):
        the_list.append(j)

task_dom = read_xml("Task.xml")
tasks_label = task_dom.createElement("Tasks")

for i in range(task_matrix.shape[1]):
    task_label = task_dom.createElement("task")
    task_label.setAttribute("ID", "Task-" + str(i))
    task_label.setAttribute("taskDetail", str(list(task_matrix[:, i])))
    task_label.setAttribute("earn", str(earn_list[i]))
    task_label.setAttribute("time_limit", str(time_list[i]))
    tasks_label.appendChild(task_label)

for j in range(task_matrix.shape[0]):
    tasks_label.setAttribute("dimension-{}-mu".format(j), str(mu_sigma_list[j][0]))
    tasks_label.setAttribute("dimension-{}-sigma".format(j), str(mu_sigma_list[j][1]))
task_dom.appendChild(tasks_label)
write_xml("Task.xml", task_dom)
