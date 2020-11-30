import external_func
import xml.dom.minidom
import sys


def read_scripts(xml_dom: xml.dom.minidom.Document):
    script_labels = xml_dom.getElementsByTagName('Script')
    script_ptr = []
    for script_label in script_labels:
        external_func.script_dict.update({script_label.getAttribute('funcName'): {
            'name': script_label.getAttribute('funcName'),
            'path': script_label.getAttribute('path'),
            'round': int(script_label.getAttribute('round')),
            'module': script_label.getAttribute('moduleName'),
        }})
        if script_label.getAttribute('path') not in sys.path:
            sys.path.append(script_label.getAttribute('path'))
        the_module = __import__(script_label.getAttribute('moduleName'),
                                fromlist=(script_label.getAttribute('funcName'),))
        script_ptr.append(eval('the_module.' + script_label.getAttribute('funcName')))
    external_func.script_func_ptrs = script_ptr
    return script_ptr


def run_script(global_dict, current_generation):
    for sc_ptr, sc_dict in zip(external_func.script_func_ptrs, external_func.script_dict.values()):
        if current_generation == sc_dict['round']:
            sc_ptr(global_dict)
