from other_tools import read_xml, write_xml

member_dom = read_xml("E:\code\PycharmProjects\execution_tool\external_file\ceMemberXml_C.xml")
primitive_labels = member_dom.getElementsByTagName("primitiveInfo") # 原子型成员标签
affector_labels = member_dom.getElementsByTagName("affectorInfo") # 影响器标签
decider_labels = member_dom.getElementsByTagName("deciderInfo") # 决策器标签
executor_labels = member_dom.getElementsByTagName("executorInfo") # 执行器标签
connector_labels = member_dom.getElementsByTagName("connectorInfo") # 联接器标签
name_list=["决策器ID","影响器ID","执行器ID","联接器ID"]

