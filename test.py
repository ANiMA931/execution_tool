from other_tools import read_xml
from matplotlib import pyplot as plt


dom = read_xml(r"E:\code\PycharmProjects\execution_tool\record_dir\data100.xml")
root = dom.documentElement
results = []
result_labels = dom.getElementsByTagName("Result")
one_attribute_dict0 = {}
one_attribute_dict1 = {}
one_attribute_dict2 = {}
a_list = [one_attribute_dict0, one_attribute_dict1, one_attribute_dict2]
for result_label, one_attribute_dict in zip(result_labels, a_list):
    records = result_label.getElementsByTagName("Record")
    for record in records:
        for key, value in record.attributes.items():
            if key not in one_attribute_dict:
                the_list = []
                the_list.append(eval(value))
                one_attribute_dict.update({key: the_list})
            else:
                one_attribute_dict[key].append(eval(value))
key_list = list(record.attributes.keys())
for idx in range(len(key_list)-1):
    plt.figure(idx)
    plt.plot(one_attribute_dict0[key_list[idx]], label='dynamic communication',color="blue", linewidth=1.5, linestyle="-")
    plt.plot(one_attribute_dict1[key_list[idx]], label='static communication',color="red", linewidth=1.5, linestyle="-")
    plt.plot(one_attribute_dict2[key_list[idx]], label='No communication',color="green", linewidth=1.5, linestyle="-")
    plt.legend(loc='upper right')
    plt.title(key_list[idx])
    plt.xlabel('generation')
    plt.ylabel(key_list[idx])
    plt.show()
