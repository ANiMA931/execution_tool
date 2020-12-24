import networkx as nx
import pattren


def read_pattern(xml_dom_for_pattern):
    """
    读取格局pattern
    :param xml_dom_for_pattern:
    :return:
    """
    pattern_label = xml_dom_for_pattern.getElementsByTagName("pattern")[0]
    pattern_comment_info = pattern_label.getElementsByTagName("commonInformation")[0]
    pattren.pattern = nx.Graph(ID=pattern_comment_info.getAttribute("ID"),
                               name=pattern_comment_info.getAttribute("name"))
    #添加格局节点信息
    node_labels = pattern_label.getElementsByTagName("position")
    for node_label in node_labels:
        pattren.pattern.add_node(node_label.getAttribute("pID"), weight=node_label.getAttribute("weight"),
                                 TYPE=node_label.getAttribute("type"), name=node_label.getAttribute("name"))

    behavior_labels=pattern_label.getElementsByTagName("behavior")
    for behavior_label in behavior_labels:
        pattren.pattern.add_edge(u_of_edge=behavior_label.getAttribute("before"), v_of_edge=behavior_label.getAttribute("after"),
                                 weight=behavior_label.getAttribute("weight"),comment=behavior_label.getAttribute("comment"))

