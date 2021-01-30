member_file_path = ''  # 成员文件路径
member_dom = None  # 成员文件xml的dom对象
primitive_dict = {}  # 保存所有原子性成员的字典
# 保存原子性成员各个组件的方法的字典
primitive_components = {
    "affector_method": None,
    "decider_method": None,
    "executor_method": None,
    "monitor_method": None,
    "connector_method": None,
}
collective_dict = {}  # 保存集合型成员的字典
# 保存集合型成员各个组件方法的字典
collective_components = {
    "decomposer_method": None,
    "converger_method": None,
    "affector_method": None,
    "decider_method": None,
    "executor_method": None,
    "monitor_method": None,
    "connector_method": None,
}
adviser_dict = {}  # 保存建议者成员的字典
adviser_method = None  # 保存建议者方法的函数指针

monitorMember_dict = {}  # 保存监控者成员的字典
monitorMember_method = None  # 保存监控者方法的函数指针
member_num = -1  # 成员数 初始化-1
network_list = []  # 保存网络的列表
network_dict = {}  # 保存网络的字典
