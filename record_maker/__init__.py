from other_tools import dict_to_xml_str, write_xml, read_xml
from xml.dom.minidom import parseString
import members
import external_func


def save_member_round_record(record_path, round_number,global_dict, width):
    member_dict = {
        'primitives': members.primitive_dict,
        'collectives': members.collective_dict,
        'advisers': members.adviser_dict,
        'monitors': members.monitor_dict,
    }
    res = "<%s>""%s""</%s>" % ("RecordDetail", dict_to_xml_str(member_dict), "RecordDetail")
    record_detail_dom = parseString(res)
    root = record_detail_dom.getElementsByTagName("RecordDetail")[0]
    root.setAttribute("round", str(round_number))
    for v in external_func.global_attribute_dict.values():
        root.setAttribute(v['aName'], str(global_dict[v['aName']]))

    write_xml(record_path + "/" + 'Record_Detail_' + str(round_number).zfill(width) + '.xml', record_detail_dom)
    print("make record in round :{}".format(round_number))


def save_global_attribute_record(record_path, round_number, global_dict):
    record_dom = read_xml(record_path + "/" + "Simulation_Record.xml")
    root = record_dom.getElementsByTagName("Result")[0]
    round_record_dom = record_dom.createElement("Record")
    for v in external_func.global_attribute_dict.values():
        round_record_dom.setAttribute(v['aName'], str(global_dict[v['aName']]))
    round_record_dom.setAttribute("round", str(round_number))
    root.appendChild(round_record_dom)
    write_xml(record_path + "/" + "Simulation_Record.xml", record_dom)
