import numpy as np
from other_tools import read_xml, write_xml
import scipy.stats as stats

dimension = 7
task_num = 200
mu_sigma_list = [(50, 15.9),
                 (30, 3.9),
                 (49, 6.7),
                 (63, 12.5),
                 (13, 6.1),
                 (54, 20.6),
                 (31, 12.2)]

task_matrix = np.zeros([dimension, task_num])
count = 0
for the_mu, the_sigma in mu_sigma_list:
    lower, upper = the_mu - 2 * the_sigma, the_mu + 2 * the_sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((lower - the_mu) / the_sigma, (upper - the_mu) / the_sigma, loc=the_mu, scale=the_sigma)
    task_matrix[count, :] = X.rvs(task_num)
    count += 1

task_dom = read_xml("Task.xml")
tasks_label = task_dom.getElementsByTagName("Tasks")[0]
for i in range(task_matrix.shape[1]):
    task_label = task_dom.createElement("task")
    task_label.setAttribute("ID","Task-"+str(i))
    task_label.setAttribute("taskDetail",str(list(task_matrix[:,i])))
    tasks_label.appendChild(task_label)


write_xml("Task.xml",task_dom)
