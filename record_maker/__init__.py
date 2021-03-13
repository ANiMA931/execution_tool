from other_tools import dict_to_xml_str, write_xml, read_xml
from xml.dom.minidom import parseString
import members
import external_func





def save_member_round_record(record_path, round_number, global_dict, width):
    """
    保存每一轮仿真所有成员的信息
    :param record_path: 仿真记录存储路径
    :param round_number: 第几回合
    :param global_dict: 保存了全局所有变量的字典
    :param width: 一共仿真的轮数
    :return: noreturn
    """
    # 整理一下所有的成员
    def save_network_round_record():
        root = record_detail_dom.getElementsByTagName("RecordDetail")[0]
        networks_label = record_detail_dom.createElement("network")
        for network_id, network_obj in members.network_dict.items():
            network_label = record_detail_dom.createElement("networkStructure")
            network_label.setAttribute("networkID", network_id)
            the_nodes = list(network_obj.nodes)
            for one_node_id in the_nodes:
                node_label = record_detail_dom.createElement("node")
                node_label.setAttribute("memberID", one_node_id)
                node_dict = dict(network_obj[one_node_id])
                for link_node_id, edge_dict in node_dict.items():
                    link_node_label = record_detail_dom.createElement("link_node")
                    link_node_label.setAttribute("memberID", link_node_id)
                    for edge_key, edge_value in edge_dict.items():
                        link_node_label.setAttribute(edge_key, str(edge_value))
                    node_label.appendChild(link_node_label)
                network_label.appendChild(node_label)
            networks_label.appendChild(network_label)
        root.appendChild(networks_label)
    member_dict = {
        'primitives': members.primitive_dict,
        'collectives': members.collective_dict,
        'advisers': members.adviser_dict,
        'monitors': members.monitorMember_dict,
    }
    # 将整理得到的所有成员保存为符合xml文档的字符串
    res = "<%s>""%s""</%s>" % ("RecordDetail", dict_to_xml_str(member_dict), "RecordDetail")
    # 将固定格式的字符串转化为dom对象
    record_detail_dom = parseString(res)
    root = record_detail_dom.getElementsByTagName("RecordDetail")[0]
    root.setAttribute("round", str(round_number))
    for v in external_func.global_attribute_dict.values():
        root.setAttribute(v['aName'], str(global_dict[v['aName']]))
    save_network_round_record()
    write_xml(record_path + "/" + 'Record_Detail_' + str(round_number).zfill(width) + '.xml', record_detail_dom)
    print("make record in round :{}".format(round_number))


def save_global_attribute_record(record_path, round_number, global_dict):
    """
    保存全局属性记录
    :param record_path:仿真记录保存路径
    :param round_number: 第几轮仿真
    :param global_dict: 保存所有变量的字典
    :return: no return
    """
    # 获取总览记录文件
    record_dom = read_xml(record_path + "/" + "Simulation_Record.xml")
    root = record_dom.getElementsByTagName("Result")[0]
    round_record_dom = record_dom.createElement("Record")
    for v in external_func.global_attribute_dict.values():
        round_record_dom.setAttribute(v['aName'], str(global_dict[v['aName']]))
    round_record_dom.setAttribute("round", str(round_number))
    root.appendChild(round_record_dom)
    write_xml(record_path + "/" + "Simulation_Record.xml", record_dom)
