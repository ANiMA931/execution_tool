import members
import xml.dom.minidom
import networkx as nx
from copy import deepcopy
from other_tools import get_empty_dict, dict2object


def read_member(member_xml_dom: xml.dom.minidom.Document):
    """
    成员读取，动态xml读取为dict
    :param member_xml_dom:xml的dom对象
    :return:四个可以保存为json的dict
    """

    affector_dict = {}  # 保存影响器的dict
    decider_dict = {}  # 保存决策器的dict
    executor_dict = {}  # 保存执行器的dict
    monitor_dict = {}  # 保存监控器的dict
    connector_dict = {}  # 保存连接器的dict

    decomposer_dict = {}  # 保存分解器的dict
    converger_dict = {}  # 保存汇聚器的dict
    c_decider_dict = {}  # 保存集合型决策器的dict
    c_executor_dict = {}  # 保存集合型执行器的dict

    a_primitives_dict = {}  # 保存原子型成员的dict
    an_advisers_dict = {}  # 保存建议者成员的dict
    a_monitorMembers_dict = {}  # 保存监控者成员的dict
    a_collective_dict = {}  # 保存集合型成员的dict

    super_label_names = ['affectorInfo', 'deciderInfo', 'executorInfo', 'monitorInfo',
                         'connectorInfo', 'decomposerInfo', 'convergerInfo', 'c_deciderInfo', 'c_executorInfo']
    label_names = ['affector', 'decider', 'executor', 'monitor',
                   'connector', 'decomposer', 'converger', 'c_decider', 'c_executor']
    components_names = ['影响器ID', '决策器ID', '执行器ID', '监控器ID', '联接器ID', '分解器ID', '汇聚器ID', '决策器ID', '执行器ID']
    components_dicts = [affector_dict, decider_dict, executor_dict, monitor_dict, connector_dict,
                        decomposer_dict, converger_dict, c_decider_dict, c_executor_dict]

    def read_member_components(xml_dom, super_label_name, label_name, components_name, components_dict):
        components_labels = xml_dom.getElementsByTagName(super_label_name)
        try:
            components_method_label = xml_dom.getElementsByTagName(label_name)[0]
            for components_label in components_labels:
                label_id = components_label.getAttribute(components_name)
                components_dict[label_id] = {}
                components_dict[label_id]['method'] = components_method_label.getAttribute('外部函数名')
                label_attribute = components_label.attributes
                for key, value in label_attribute.items():
                    try:
                        components_dict[label_id][key] = eval(value)
                    # except EOFError:
                    #     components_dict[label_id][key] = value
                    except NameError:
                        components_dict[label_id][key] = value
                    except EOFError:
                        components_dict[label_id][key] = None
        except IndexError:  # 当某个标签不存在时
            pass

    # def read_affector(xml_dom_for_affector):
    #     """
    #     读取影响器
    #     :param xml_dom_for_affector:
    #     :return:
    #     """
    #     affector_labels = xml_dom_for_affector.getElementsByTagName('affectorInfo')
    #     affector_method_label = xml_dom_for_affector.getElementsByTagName('affector')[0]
    #     for affector_label in affector_labels:
    #         label_id = affector_label.getAttribute('影响器ID')
    #         # affector_dict.update({label_id: {}})
    #         affector_dict[label_id] = {}
    #         # affector_dict[label_id].update({'method': affector_method_label.getAttribute('外部函数名')})
    #         affector_dict[label_id]['method'] = affector_method_label.getAttribute('外部函数名')
    #         label_attribute = affector_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # affector_dict[label_id].update({key: eval(value)})
    #                 affector_dict[label_id][key] = eval(value)
    #             except NameError:
    #                 # affector_dict[label_id].update({key: value})
    #                 affector_dict[label_id][key] = value
    #
    # read_affector(member_xml_dom)

    # def read_decider(xml_dom_for_decider):
    #     """
    #     读取决策器
    #     :param xml_dom_for_decider:
    #     :return:
    #     """
    #     decider_labels = xml_dom_for_decider.getElementsByTagName('deciderInfo')
    #     decider_method_label = xml_dom_for_decider.getElementsByTagName('decider')[0]
    #     for decider_label in decider_labels:
    #         label_id = decider_label.getAttribute('决策器ID')
    #         # decider_dict.update({label_id: {}})
    #         decider_dict[label_id] = {}
    #         # decider_dict[label_id].update({'method': decider_method_label.getAttribute('外部函数名')})
    #         decider_dict[label_id]['method'] = decider_method_label.getAttribute('外部函数名')
    #         label_attribute = decider_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # decider_dict[label_id].update({key: eval(value)})
    #                 decider_dict[label_id][key] = eval(value)
    #             except:
    #                 # decider_dict[label_id].update({key: value})
    #                 decider_dict[label_id][key] = value
    #
    # read_decider(member_xml_dom)

    # def read_executor(xml_dom_for_executor):
    #     """
    #     读取执行器
    #     :param xml_dom_for_executor:
    #     :return:
    #     """
    #     executor_labels = xml_dom_for_executor.getElementsByTagName('executorInfo')
    #     executor_method_label = xml_dom_for_executor.getElementsByTagName('executor')[0]
    #     for executor_label in executor_labels:
    #         label_id = executor_label.getAttribute('执行器ID')
    #         # executor_dict.update({label_id: {}})
    #         executor_dict[label_id] = {}
    #         # executor_dict[label_id].update({'method': executor_method_label.getAttribute('外部函数名')})
    #         executor_dict[label_id]['method'] = executor_method_label.getAttribute('外部函数名')
    #         label_attribute = executor_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # executor_dict[label_id].update({key: eval(value)})
    #                 executor_dict[label_id][key] = eval(value)
    #
    #             except NameError:
    #                 # executor_dict[label_id].update({key: value})
    #                 executor_dict[label_id][key] = value
    #
    # read_executor(member_xml_dom)

    # def read_monitor(xml_dom_for_monitor):
    #     """
    #     读取监控器
    #     :param xml_dom_for_monitor:
    #     :return:
    #     """
    #     monitor_labels = xml_dom_for_monitor.getElementsByTagName('monitorInfo')
    #     monitor_method_label = xml_dom_for_monitor.getElementsByTagName('monitor')[0]
    #     for monitor_label in monitor_labels:
    #         label_id = monitor_label.getAttribute('监控器ID')
    #         # monitor_dict.update({label_id: {}})
    #         monitor_dict[label_id] = {}
    #         # monitor_dict[label_id].update({'method': monitor_method_label.getAttribute('外部函数名')})
    #         monitor_dict[label_id]['method'] = monitor_method_label.getAttribute('外部函数名')
    #         label_attribute = monitor_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # monitor_dict[label_id].update({key: eval(value)})
    #                 monitor_dict[label_id][key] = eval(value)
    #
    #             except NameError:
    #                 # monitor_dict[label_id].update({key: value})
    #                 monitor_dict[label_id][key] = value
    #
    # read_monitor(member_xml_dom)
    #
    # def read_connector(xml_dom_for_connector):
    #     """
    #     读取连接器
    #     :param xml_dom_for_connector:
    #     :return:
    #     """
    #     connector_labels = xml_dom_for_connector.getElementsByTagName('connectorInfo')
    #     connector_method_label = xml_dom_for_connector.getElementsByTagName('connector')[0]
    #     for connector_label in connector_labels:
    #         label_id = connector_label.getAttribute('联接器ID')
    #         # connector_dict.update({label_id: {}})
    #         connector_dict[label_id] = {}
    #         # connector_dict[label_id].update({'method': connector_method_label.getAttribute('外部函数名')})
    #         connector_dict[label_id]['method'] = connector_method_label.getAttribute('外部函数名')
    #         label_attribute = connector_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # connector_dict[label_id].update({key: eval(value)})
    #                 connector_dict[label_id][key] = eval(value)
    #
    #             except NameError:
    #                 # connector_dict[label_id].update({key: value})
    #                 connector_dict[label_id][key] = value
    #
    # read_connector(member_xml_dom)

    def read_primitive(xml_dom_for_primitive):
        """
        读取原子型成员
        :param xml_dom_for_primitive:
        :return:
        """
        primitives_labels = xml_dom_for_primitive.getElementsByTagName('primitiveInfo')
        for primitives_label in primitives_labels:
            label_id = primitives_label.getAttribute('原子型成员ID')
            # a_primitives_dict.update({label_id: {}})
            a_primitives_dict[label_id] = {}
            label_attribute = primitives_label.attributes
            for key, value in label_attribute.items():
                try:
                    # a_primitives_dict[label_id].update({key: eval(value)})
                    a_primitives_dict[label_id][key] = eval(value)
                except NameError:
                    # a_primitives_dict[label_id].update({key: value})
                    a_primitives_dict[label_id][key] = value
                except SyntaxError:  # 当某一个标签属性存在但值为空时
                    a_primitives_dict[label_id][key] = None
            try:
                # 配置影响器
                a_primitives_dict[label_id]['影响器'] = affector_dict[a_primitives_dict[label_id]['影响器']]
            except KeyError:  # 有的内容是空，已经提前设置为None 了所以不用处理
                pass

            try:
                # 配置决策器
                a_primitives_dict[label_id]['决策器'] = decider_dict[a_primitives_dict[label_id]['决策器']]
            except KeyError:  # 有的内容是空，已经提前设置为None 了所以不用处理
                pass

            try:
                # 配置监控器
                a_primitives_dict[label_id]['监控器'] = monitor_dict[a_primitives_dict[label_id]['监控器']]
            except KeyError:  # 有的内容是空，已经提前设置为None 了所以不用处理
                pass

            try:
                # 配置执行器
                a_primitives_dict[label_id]['执行器'] = executor_dict[a_primitives_dict[label_id]['执行器']]
            except KeyError:  # 有的内容是空，已经提前设置为None 了所以不用处理
                pass

            try:
                # 配置连接器
                a_primitives_dict[label_id]['联接器'] = connector_dict[a_primitives_dict[label_id]['联接器']]
            except KeyError:  # 有的内容是空，已经提前设置为None 了所以不用处理
                pass
            # # 初始化与原子型单元的连接
            # # a_primitives_dict[label_id].update({'conn_primitive': {}})
            # a_primitives_dict[label_id]['conn_primitive'] = {}
            # # 初始化与集合型单元的连接
            # # a_primitives_dict[label_id].update({'conn_collective': {}})
            # a_primitives_dict[label_id]['conn_collective'] = {}
            # # 初始化与建议者单元的连接
            # # a_primitives_dict[label_id].update({'conn_adviser': {}})
            # a_primitives_dict[label_id]['conn_adviser'] = {}
            # # 初始化与监控者单元的连接
            # # a_primitives_dict[label_id].update({'conn_monitorMember': {}})
            # a_primitives_dict[label_id]['conn_monitorMember'] = {}

    def read_advisers(xml_dom_for_adviser):
        """
        读取建议者
        :param xml_dom_for_adviser:
        :return:
        """
        adviserInfo_labels = xml_dom_for_adviser.getElementsByTagName('advisorInfo')
        for adviserInfo_label in adviserInfo_labels:
            label_id = adviserInfo_label.getAttribute('建议者ID')
            # an_advisers_dict.update({label_id: {}})
            an_advisers_dict[label_id] = {}
            label_attribute = adviserInfo_label.attributes
            for key, value in label_attribute.items():
                try:
                    # an_advisers_dict[label_id].update({key: eval(value)})
                    an_advisers_dict[label_id][key] = eval(value)
                except NameError:
                    # an_advisers_dict[label_id].update({key: value})
                    an_advisers_dict[label_id][key] = value
                except EOFError:
                    an_advisers_dict[label_id][key] = None
            # 初始化与原子型单元的连接
            # # an_advisers_dict[label_id].update({'conn_primitive': {}})
            # an_advisers_dict[label_id]['conn_primitive'] = {}
            # # 初始化与集合型单元的连接
            # # an_advisers_dict[label_id].update({'conn_collective': {}})
            # an_advisers_dict[label_id]['conn_collective'] = {}

        # 本段代码是为了能够将xml里的成员对象由dict变更为类对象，但是不支持中文，故暂时作罢
        #     an_advisers_dict[label_id]['__class__'] = 'Adviser'
        #     an_advisers_dict[label_id]['__module__']='members.read_file'
        # empty_adviser = get_empty_dict(an_advisers_dict[label_id])
        # members.Adviser = type('Adviser', (object,), empty_adviser)
        # a_adviser = dict2object(an_advisers_dict[label_id])

    def read_monitorMembers(xml_dom_for_monitorMember):
        """
        读取监控者
        :param xml_dom_for_monitorMember:
        :return:
        """
        monitorMembers_labels = xml_dom_for_monitorMember.getElementsByTagName('monitorMemberInfo')
        for monitorMembers_label in monitorMembers_labels:
            label_id = monitorMembers_label.getAttribute('监控者ID')
            # a_monitorMembers_dict.update({label_id: {}})
            a_monitorMembers_dict[label_id] = {}
            label_attribute = monitorMembers_label.attributes
            for key, value in label_attribute.items():
                try:
                    # a_monitorMembers_dict[label_id].update({key: eval(value)})
                    a_monitorMembers_dict[label_id][key] = eval(value)
                except NameError:
                    # a_monitorMembers_dict[label_id].update({key: value})
                    a_monitorMembers_dict[label_id][key] = value
                except EOFError:
                    a_monitorMembers_dict[label_id][key] = None
            # # 初始化与原子型单元的连接
            # # a_monitorMembers_dict[label_id].update({'conn_primitive': {}})
            # a_monitorMembers_dict[label_id]['conn_primitive'] = {}
            # # 初始化与集合型单元的连接
            # # a_monitorMembers_dict[label_id].update({'conn_collective': {}})
            # a_monitorMembers_dict[label_id]['conn_collective'] = {}

    # def read_decomposer(xml_dom_for_decomposer):
    #     """
    #     读取分解器
    #     :param xml_dom_for_decomposer:
    #     :return:
    #     """
    #     decomposer_labels = xml_dom_for_decomposer.getElementsByTagName('decomposerInfo')
    #     decomposer_method_label = xml_dom_for_decomposer.getElementsByTagName('decomposer')[0]
    #     for decomposer_label in decomposer_labels:
    #         label_id = decomposer_label.getAttribute('分解器ID')
    #         # decomposer_dict.update({label_id: {}})
    #         decomposer_dict[label_id] = {}
    #         # decomposer_dict[label_id].update({'method': decomposer_method_label.getAttribute('外部函数名')})
    #         decomposer_dict[label_id]['method'] = decomposer_method_label.getAttribute('外部函数名')
    #         label_attribute = decomposer_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # decomposer_dict[label_id].update({key: eval(value)})
    #                 decomposer_dict[label_id][key] = eval(value)
    #             except NameError:
    #                 # decomposer_dict[label_id].update({key: value})
    #                 decomposer_dict[label_id][key] = value
    #
    # read_decomposer(member_xml_dom)
    #
    # def read_converger(xml_dom_for_converger):
    #     converger_labels = xml_dom_for_converger.getElementsByTagName('convergerInfo')
    #     converger_method_label = xml_dom_for_converger.getElementsByTagName('converger')[0]
    #     for converger_label in converger_labels:
    #         label_id = converger_label.getAttribute('汇聚器ID')
    #         # converger_dict.update({label_id: {}})
    #         converger_dict[label_id] = {}
    #         # converger_dict[label_id].update({'method': converger_method_label.getAttribute('外部函数名')})
    #         converger_dict[label_id]['method'] = converger_method_label.getAttribute('外部函数名')
    #         label_attribute = converger_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # converger_dict[label_id].update({key: eval(value)})
    #                 converger_dict[label_id][key] = eval(value)
    #             except NameError:
    #                 # converger_dict[label_id].update({key: value})
    #                 converger_dict[label_id][key] = value
    #
    # read_converger(member_xml_dom)
    #
    #
    # def read_c_decider(xml_dom_for_c_decider):
    #     c_decider_labels = xml_dom_for_c_decider.getElementsByTagName('c_deciderInfo')
    #     c_decider_method_label = xml_dom_for_c_decider.getElementsByTagName('c_decider')[0]
    #     for c_decider_label in c_decider_labels:
    #         label_id = c_decider_label.getAttribute('决策器ID')
    #         # c_decider_dict.update({label_id: {}})
    #         c_decider_dict[label_id] = {}
    #         # c_decider_dict[label_id].update({'method': c_decider_method_label.getAttribute('外部函数名')})
    #         c_decider_dict[label_id]['method'] = c_decider_method_label.getAttribute('外部函数名')
    #         label_attribute = c_decider_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # c_decider_dict[label_id].update({key: eval(value)})
    #                 c_decider_dict[label_id][key] = eval(value)
    #             except NameError:
    #                 # c_decider_dict[label_id].update({key: value})
    #                 c_decider_dict[label_id][key] = value
    #
    # read_c_decider(member_xml_dom)
    #
    #
    # def read_c_executor(xml_dom_for_c_executor):
    #     c_executor_labels = xml_dom_for_c_executor.getElementsByTagName('c_executorInfo')
    #     c_executor_method_label = xml_dom_for_c_executor.getElementsByTagName('c_executor')[0]
    #     for c_executor_label in c_executor_labels:
    #         label_id = c_executor_label.getAttribute('执行器ID')
    #         # c_executor_dict.update({label_id: {}})
    #         c_executor_dict[label_id] = {}
    #         # c_executor_dict[label_id].update({'method': c_executor_method_label.getAttribute('外部函数名')})
    #         c_executor_dict[label_id]['method'] = c_executor_method_label.getAttribute('外部函数名')
    #         label_attribute = c_executor_label.attributes
    #         for key, value in label_attribute.items():
    #             try:
    #                 # c_executor_dict[label_id].update({key: eval(value)})
    #                 c_executor_dict[label_id][key] = eval(value)
    #             except NameError:
    #                 # c_executor_dict[label_id].update({key: value})
    #                 c_executor_dict[label_id][key] = value
    #
    # read_c_executor(member_xml_dom)

    def read_collective(xml_dom_for_collective):
        """
        读取集合型成员
        :param xml_dom_for_collective:
        :return:
        """
        collective_labels = xml_dom_for_collective.getElementsByTagName('collectiveInfo')
        for collective_label in collective_labels:
            label_id = collective_label.getAttribute('集合型成员ID')
            # a_collective_dict.update({label_id: {}})
            a_collective_dict[label_id] = {}
            label_attribute = collective_label.attributes
            for key, value in label_attribute.items():
                try:
                    # a_collective_dict[label_id].update({key: eval(value)})
                    a_collective_dict[label_id][key] = eval(value)
                except NameError:
                    # a_collective_dict[label_id].update({key: value})
                    a_collective_dict[label_id][key] = value
                except EOFError:
                    a_collective_dict[label_id][key] = None

            try:
                # 配置影响器
                a_collective_dict[label_id]['影响器'] = affector_dict[a_collective_dict[label_id]['影响器']]
            except KeyError:
                pass

            try:
                # 配置分解器
                a_collective_dict[label_id]['分解器'] = decomposer_dict[a_collective_dict[label_id]['分解器']]
            except KeyError:
                pass

            try:
                # 配置汇聚器
                a_collective_dict[label_id]['汇聚器'] = converger_dict[a_collective_dict[label_id]['汇聚器']]
            except KeyError:
                pass

            try:
                # 配置决策器
                a_collective_dict[label_id]['决策器'] = c_decider_dict[a_collective_dict[label_id]['决策器']]
            except KeyError:
                pass

            try:
                # 配置执行器
                a_collective_dict[label_id]['执行器'] = c_executor_dict[a_collective_dict[label_id]['执行器']]
            except KeyError:
                pass

            try:
                # 配置监控器
                a_collective_dict[label_id]['监控器'] = monitor_dict[a_collective_dict[label_id]['监控器']]
            except KeyError:
                pass

            try:
                # 配置连接器
                a_collective_dict[label_id]['联接器'] = connector_dict[a_collective_dict[label_id]['联接器']]
            except KeyError:
                pass
            # 初始化与原子型单元的连接
            # # a_collective_dict[label_id].update({'conn_primitive': {}})
            # a_collective_dict[label_id]['conn_primitive'] = {}
            # # 初始化与集合型单元的连接
            # # a_collective_dict[label_id].update({'conn_collective': {}})
            # a_collective_dict[label_id]['conn_collective'] = {}
            # # 初始化与建议者单元的连接
            # # a_collective_dict[label_id].update({'conn_adviser': {}})
            # a_collective_dict[label_id]['conn_adviser'] = {}
            # # 初始化与监控者单元的连接
            # # a_collective_dict[label_id].update({'conn_monitorMember': {}})
            # a_collective_dict[label_id]['conn_monitorMember'] = {}

    for super_label_name, label_name, components_name, components_dict in \
            zip(super_label_names, label_names, components_names, components_dicts):
        read_member_components(member_xml_dom, super_label_name, label_name, components_name, components_dict)

    read_advisers(member_xml_dom)
    read_monitorMembers(member_xml_dom)
    read_primitive(member_xml_dom)
    read_collective(member_xml_dom)

    members.primitive_dict = a_primitives_dict
    members.collective_dict = a_collective_dict
    members.adviser_dict = an_advisers_dict
    members.monitor_dict = a_monitorMembers_dict
    # members.old_primitive_dict = deepcopy(members.primitive_dict)
    # members.old_collective_dict = deepcopy(members.collective_dict)
    # members.old_adviser_dict = deepcopy(members.adviser_dict)
    # members.old_monitor_dict = deepcopy(members.monitor_dict)
    return a_primitives_dict, an_advisers_dict, a_monitorMembers_dict, a_collective_dict


def read_network(member_xml_dom: xml.dom.minidom.Document):
    network_labels = member_xml_dom.getElementsByTagName('networkStructure')
    for network_label in network_labels:
        G = nx.DiGraph(TYPE=network_label.getAttribute('type'), ID=network_label.getAttribute('ID'))
        edges_labels = network_label.getElementsByTagName('connectInfo')
        for edges_label in edges_labels:
            G.add_edge(edges_label.getAttribute('from'), edges_label.getAttribute('to'),
                       strength=float(edges_label.getAttribute('strength')))
        members.network_list.append(G)
    members.old_network_list = members.network_list.copy()
