# import external_func
# import members
# from members.read_file import read_member, read_network
# from other_tools import read_xml
# import networkx as nx
# import matplotlib.pyplot as plt
# from external_func.read_file import read_global_attribute, read_round_method, read_round_number

# external_func.external_func_file_path = r'external_file_for_cEvolution\simulation_definition.xml'  # 外部输入的文件名
# members.member_file_path = r'external_file_for_cEvolution\fpMemberXml_C.xml'
# 
# external_func.external_func_dom = read_xml(external_func.external_func_file_path)
# members.member_dom = read_xml(members.member_file_path)
# read_member(members.member_dom)
# func_ptrs = read_global_attribute(external_func.external_func_dom, globals())
# read_round_method(external_func.external_func_dom)
# read_round_number(external_func.external_func_dom)
# external_func.round_method_dict['attributes']['num']=1
# external_func.round_method(external_func.round_method_dict['attributes'])
# for global_func in func_ptrs:
#     global_func(**external_func.global_attribute_dict[global_func.__name__]['attributes'])
#     print()
# 

# if __name__ == '__main__':
#     members.member_file_path=r'F:\pythonCode\PycharmProjects\execution_tool\external_file_for_cEvolution\fpMemberXml_C.xml'
#     read_network(read_xml(members.member_file_path))
#     for i in range(members.network_list.__len__()):
#         plt.figure(members.network_list[i].graph['ID'])
#         nx.draw(members.network_list[i], with_labels=True, font_weight='bold')
#         plt.get_current_fig_manager().window.state('zoomed')
#     plt.show()

import copy
D={'name':{'first':'zhang','last':'san'},'jobs':['IT','HR']}#原始字典含有嵌套对象
C1=D
C2=copy.deepcopy(D)#深拷贝
C1['name']['first']='data'#改变原始字典中的jobs子对象‘it'变为’data'
print(D,'\n',C1,'\n',C2)


# def dict_to_xml_str(params):
#     str = ""
#     for k, v in params.items():
#         str += "<%s>""%s""</%s>" % (k, v, k) if not isinstance(v, dict) else "<%s>""%s""</%s>" % (k, dict_to_xml_str(v), k)
#     message = "<MbfBody>" + str + "</MbfBody>"
#     return message
#
#
# if __name__ == '__main__':
#     params = {"name": "小明", "age": 18, "hobby": "football", "other": {"name": "火云邪神"}}
#     print(dict_to_xml_str(params))