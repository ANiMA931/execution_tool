# simulation_tool.py
'''
本文件是写的界面与部分界面的设置
'''
from UI.simulation_exe_Form import Ui_Form  # 用designer设计的界面类
from PyQt5 import QtCore, QtGui, QtWidgets  # Qt的核心部件
from matplotlib import pyplot as plt
import networkx as nx

import sys  # 需要的部分内容
import os  # 需要的部分内容

import xml.dom.minidom  # 系统使用的xml操作类
from xml.dom.minidom import parseString
import external_func  # 自己编写的外部函数模块
import members  # 自己编写的成员模块
import pattren

from external_func.read_file import read_xml_to_module  # 单独引用一下读取模块中的总和函数
from external_func.__scripts import read_scripts, run_script  # 单独引用一下脚本模块中读取与运行的函数
from time import sleep  # 测试可能需要的东西
from datetime import datetime
from members.read_file import read_network, read_member
from pattren.read_file import read_pattern
from other_tools import read_xml, write_xml  # 读取与生成xml文件的方法
from record_maker import save_member_round_record, save_global_attribute_record

inherited = bool()  


class MyThread(QtCore.QThread):
    _signal = QtCore.pyqtSignal(int)

    def __init__(self, generation_upper, global_dict):
        super(MyThread, self).__init__()
        self.current_generation = 0
        self.generation_upper = generation_upper
        self.global_dict = global_dict
        self.flag = False

    def run(self):
        while self.current_generation < self.generation_upper:
            if self.flag:
                self.current_generation += 1
                if inherited:
                    pass
                else:
                    load_old(self.global_dict)
                run_script(self.global_dict, self.current_generation)
                print("in Thread, current_generation:{}".format(self.current_generation))
                external_func.round_method(self.global_dict)
                self._signal.emit(self.current_generation)
                sleep(0.001)
            else:
                continue


def load_old(global_dict):
    external_func.global_attribute_dict = external_func.old_global_attribute_dict.copy()
    for k, v in external_func.global_attribute_dict.items():
        global_dict[v['aName']] = v['val']
    read_member(members.member_dom)
    read_network(members.member_dom)


class uf_Form(QtWidgets.QWidget, Ui_Form):

    def __init__(self, global_dict):
        super(uf_Form, self).__init__()
        # 加载UI
        self.MyThread = MyThread(0, global_dict)
        self.global_dict = global_dict
        self.setupUi(self)
        # 对UI中的部分控件进行设置
        self.setupUiAgain()
        # 加载本界面需要的一些资源
        self.setupResoure()
        # 设置所有的信号
        self.set_all_signal()
        # 设置所有的槽函数
        self.set_all_slot()
        # 设置不可更改窗口大小
        self.setFixedSize(self.width(), self.height())
        self.current_generation = 0
        self.flag = "waiting"
        self.start_moment = None
        self.end_moment = 0

    def set_all_slot(self):
        """
        设置所有的槽函数
        :return: no return
        """
        # 添加行按钮槽函数
        self.add_script_button.clicked.connect(self.slot_btn_add_oneRow)
        # 删除行按钮槽函数
        self.delete_script_button.clicked.connect(self.slot_btn_delete_oneRow)
        # 加载脚本按钮槽函数
        self.load_script_button.clicked.connect(self.slot_btn_load_script)
        # 重新设置脚本按钮槽函数
        self.reset_script_button.clicked.connect(self.slot_btn_reset_script)
        # 设置成员文件路径按钮槽函数
        self.members_filedialog_btn.clicked.connect(self.slot_btn_set_members_path)
        # 设置仿真定义文件路径按钮槽函数
        self.record_filedialog_btn.clicked.connect(self.slot_btn_set_record_path)
        # 设置表格脚本函数路径双击槽函数
        self.script_table_widget.itemDoubleClicked.connect(self.slot_btn_load_script_file_path)
        # 设置存储路径函数
        self.def_xml_filedialog_btn.clicked.connect(self.slot_btn_set_definition_path)
        # 设置轮方法槽函数
        self.start_btn.clicked.connect(self.emit_round_method)
        # 设置暂停槽函数
        self.pause_btn.clicked.connect(self.slot_btn_pause)
        # 设置终止槽函数
        self.stop_btn.clicked.connect(self.slot_terminate_simulation)
        # 设置显示网络函数
        self.show_nw_btn.clicked.connect(self.slot_btn_show_network)
        # 设置测试用按钮
        self.testButton.clicked.connect(self.slot_test_button)
        self.testButton.hide()
        ...

    def set_all_signal(self):
        self.MyThread._signal.connect(self.slot_return_from)
        # self.MyThread.finished.connect(a)
        ...

    def setupResoure(self):
        """
        设置窗口需要的各种资源
        :return: no return
        """
        # 播放按钮的图标
        self.start_btn_icon = QtGui.QIcon(r'.\UI\播放按钮.ico')
        # 暂停按钮的图标
        self.pause_btn_icon = QtGui.QIcon(r'.\UI\暂停.ico')
        # 停止按钮的图标
        self.stop_btn_icon = QtGui.QIcon(r'.\UI\停止.ico')
        # 初始化设置，将播放按钮图标设置为启动仿真的按钮
        self.start_btn.setIcon(self.start_btn_icon)
        self.pause_btn.setIcon(self.pause_btn_icon)
        # 初始化设置，将停止按钮的图标设置为停止仿真的按钮
        self.stop_btn.setIcon(self.stop_btn_icon)

    def setupUiAgain(self):
        """
        设置窗口中各种元素的编辑于排版
        :return:
        """
        # 脚本注册表的所有内容均靠左对齐
        self.script_table_widget.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
        self.script_table_widget.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
        self.script_table_widget.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
        # 设置脚本注册表三列的宽度
        self.script_table_widget.setColumnWidth(0, 100)
        self.script_table_widget.setColumnWidth(1, 200)
        self.script_table_widget.setColumnWidth(2, 538)
        # 设置脚本注册表行标可视
        self.script_table_widget.verticalHeader().setVisible(True)
        self.pause_btn.setEnabled(False)
        # 设置日期编辑栏获取当前日期
        self.modify_dateEdit.setDate(QtCore.QDate.currentDate())
        # self.script_table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def all_fill(self):
        """
        判断脚本注册表内容是否填满。
        :return: bool
        """
        # 获取行列数值
        rows_num = self.script_table_widget.rowCount()
        columns_num = self.script_table_widget.columnCount()
        # 双层循环判断对比
        for row in range(rows_num):
            for col in range(columns_num):
                # 如果循环的当前表格对应的item的内容为空，则返回False，表示未填满
                if self.script_table_widget.item(row, col).text() is "":
                    return False
        # 均通过判断，说明表格已经被填满，具备保存逻辑
        return True

    def slot_btn_load_script_file_path(self):
        """
        槽函数，用来保存已经注册的所有脚本函数为XML文件。
        :return:
        """
        # 判断当前表格可编辑，则表示未保存已有内容
        if self.add_script_button.isEnabled() and self.delete_script_button.isEnabled():
            # 获取单圈选中的表格里item对象
            item = self.script_table_widget.selectedItems()[0]
            # 双层循环嵌套遍历表格
            for row in range(self.script_table_widget.rowCount()):
                for col in range(self.script_table_widget.columnCount()):
                    # 判断选中的表格里item是否为第二列，即需要设置脚本函数所在文件路径的列且内容为空
                    if item == self.script_table_widget.item(row, col) and col == 2 and item.text() == "":
                        # 打开文件对话框，选择.py文件
                        py_scripts_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择脚本py文件", "./",
                                                                                "XML Files (*.py);;All Files (*)")
                        # 当成功选择了一个文件时，设置路径
                        if py_scripts_path[0] is not "":
                            item.setText(py_scripts_path[0])
                        # 服务信息更新显示
                        self.service_msg_log_text.append(
                            str(datetime.now()) + ': ' + 'Read script from: ' + py_scripts_path[0])
                        return

    def slot_btn_load_script(self):
        """
        保存已经设置的脚本信息为xml文件槽函数
        :return:
        """
        # 设置将表格中的内容按列保存为xml
        if self.all_fill() and self.save_scripts_to_xml():
            # 设置脚本表格不可编辑
            self.script_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.add_script_button.setEnabled(False)
            self.delete_script_button.setEnabled(False)
            # 一点提示信息
            self.script_setting_widget_status_label.setText("Script loaded.")
            QtWidgets.QMessageBox.information(self, 'Success', 'Scripts save succeed.')
            read_scripts(xml_dom=read_xml(external_func.scripts_file_path))
        else:
            QtWidgets.QMessageBox.warning(self, 'failure', 'Scripts save failed.\n Please check the form.')

    def slot_btn_reset_script(self):
        """
        重新设定脚本列表
        :return: no return
        """
        # 设置脚本表格可双击编辑
        self.script_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        # 一点提示信息
        QtWidgets.QMessageBox.information(self, 'Reset', 'You can reset Scripts now.')
        # 设置添加按钮与删除按钮可用
        self.add_script_button.setEnabled(True)
        self.delete_script_button.setEnabled(True)
        # 更改一下标签状态
        self.script_setting_widget_status_label.setText("Script setting. ")

    def slot_btn_add_oneRow(self):
        """
        表格加一行槽函数
        :return: no return
        """
        # 首先获取一下行列数
        rows_num = self.script_table_widget.rowCount()
        columns_num = self.script_table_widget.columnCount()
        # 表格行数+1
        self.script_table_widget.setRowCount(self.script_table_widget.rowCount() + 1)
        # 对新添加的一行，每一列赋一个新的item
        for col in range(columns_num):
            item_data = QtWidgets.QTableWidgetItem("")
            self.script_table_widget.setItem(rows_num, col, item_data)

    def slot_btn_delete_oneRow(self):
        """
        删除脚本表一行
        :return: no return
        """
        # 表格数-1，已有的item会自动删除
        self.script_table_widget.setRowCount(self.script_table_widget.rowCount() - 1)

    def slot_btn_set_definition_path(self):
        """
        设置仿真定义文件路径
        :return: no return
        """
        try:
            xml_definition_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择仿真定义xml文件", "./",
                                                                        "XML Files (*.xml);;All Files (*)")
            self.def_xml_path_edit.setText(xml_definition_path[0])
            definition_dom = read_xml(xml_definition_path[0])
            external_func.external_func_file_path = xml_definition_path[0]
            read_xml_to_module(definition_dom, self.global_dict)
            external_func.round_method_dict['attributes']['num'] = 16549
            member_path_label = definition_dom.getElementsByTagName("memberModelFilePath")[0]
            self.members_xml_path_edit.setText(member_path_label.firstChild.data)
            def_id_label = definition_dom.getElementsByTagName("simulationExecutionMetaModel")[0]
            self.definition_ID_edit.setText(def_id_label.firstChild.data)
            member_meta_label = definition_dom.getElementsByTagName("memberMetaModelFilePath")[0]
            self.meta_member_ID_edit.setText(member_meta_label.firstChild.data)
            generation_label = definition_dom.getElementsByTagName("simulationRoundNumber")[0]
            self.generation_Edit.setText(generation_label.firstChild.data)
            self.MyThread.generation_upper = int(generation_label.firstChild.data)
            inherited_label = definition_dom.getElementsByTagName("inherited")[0]
            global inherited
            if int(inherited_label.firstChild.data):
                self.inherited_Edit.setText("True")
                inherited = True
            else:
                self.inherited_Edit.setText("False")
                inherited = False
            # 根据这个路径来读取成员
            member_dom = read_xml(self.members_xml_path_edit.text())
            # 服务信息更新显示
            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + 'Read member from: ' + self.members_xml_path_edit.text())
            # 解析成员
            # global net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c
            # net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c = net_work_read(member_dom)
            # global primitives, advisers, monitorMembers, collectives
            # primitives, advisers, monitorMembers, collectives = member_read(member_dom)
            # 读取一下各个成员的数目与基本信息，并在界面上显示
            id_role_dict, member_number, p_number, c_number, a_number, m_number = format_members_id_role(member_dom)
            read_member(member_dom)
            read_network(member_dom)
            read_pattern(member_dom)

            members.member_dom = member_dom
            members.member_file_path = self.members_xml_path_edit.text()
            members.member_num = member_number
            self.reset_member_tableWidget(member_number, id_role_dict)
            self.primitive_num_edit.setText(str(p_number))
            self.adviser_num_edit.setText(str(a_number))
            self.monitor_num_edit.setText(str(m_number))
            self.collective_num_edit.setText(str(c_number))
            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + "Primitive:{}|Adviser:{}|Monitor:{}|Collective:{}".format(
                    p_number, a_number, m_number, c_number
                ))

            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + 'Read definition from: ' + member_path_label.firstChild.data)
        except:
            QtWidgets.QMessageBox.critical(self, "error", "Definition file error!")
            self.def_xml_path_edit.clear()
            self.service_msg_log_text.append(str(datetime.now()) + ': ' + 'Setting definition file error. ')

    def slot_btn_set_members_path(self):
        """
        读取所有成员的路径的槽函数
        :return: no return
        """
        try:
            # 打开文件对话框
            xml_members_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择仿真成员xml文件", "./",
                                                                     "XML Files (*.xml);;All Files (*)")
            self.members_xml_path_edit.setText(xml_members_path[0])
            # 根据这个路径来读取成员
            member_dom = read_xml(self.members_xml_path_edit.text())
            members.member_file_path = self.members_xml_path_edit.text()
            # 服务信息更新显示
            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + 'Read member from: ' + self.members_xml_path_edit.text())
            # 解析成员
            # global net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c
            # net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c = net_work_read(member_dom)
            # global primitives, advisers, monitorMembers, collectives
            # primitives, advisers, monitorMembers, collectives = member_read(member_dom)
            # 读取一下文件中的成员基本信息与数目，并在界面上刷新显示
            id_role_dict, member_number, p_number, c_number, a_number, m_number = format_members_id_role(member_dom)
            read_member(member_dom)
            read_network(member_dom)
            read_pattern(member_dom)

            members.member_dom = member_dom
            members.member_file_path = self.members_xml_path_edit.text()
            members.member_num = member_number
            self.reset_member_tableWidget(member_number, id_role_dict)
            self.primitive_num_edit.setText(str(p_number))
            self.adviser_num_edit.setText(str(a_number))
            self.monitor_num_edit.setText(str(m_number))
            self.collective_num_edit.setText(str(c_number))
            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + "Primitive:{}|Adviser:{}|Monitor:{}|Collective:{}".format(
                    p_number, a_number, m_number, c_number
                ))
        except:
            QtWidgets.QMessageBox.critical(self, "Error", "Member file error!")
            self.members_xml_path_edit.clear()
            self.service_msg_log_text.append(str(datetime.now()) + ': ' + 'Setting member XML file error. ')
            raise

    def slot_btn_pause(self):
        self.flag = "waiting"
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.MyThread.flag = False
        self.MyThread.wait()

    def slot_return_from(self, current):
        # 一个迭代的仿真结束了，需要判断一下仿真是否需要继承数据。
        self.current_generation = current
        # print("in widget, current_generation:{}".format(self.current_generation))
        self.exe_progress_bar.setValue(self.current_generation / external_func.round_number * 100)
        if current == external_func.round_number:
            self.slot_btn_pause()
            self.end_moment = datetime.now()
            self.service_msg_log_text.append(str(self.end_moment) + ": Simulation task completed.")
            record_dom = read_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml")
            record_dom_root = record_dom.getElementsByTagName("Result")[0]
            record_dom_root.setAttribute("EndMoment", str(self.end_moment))
            record_dom_root.setAttribute("TimeConsuming", str(self.end_moment - self.start_moment))
            write_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml", record_dom)
        if current % int(self.step_size_Edit.text()) == 0:
            self.MyThread.flag = False
            save_member_round_record(self.record_dir_path_edit.text(), current, self.global_dict,
                                     len(self.generation_Edit.text()))
            save_global_attribute_record(self.record_dir_path_edit.text(), current, self.global_dict)
            self.MyThread.flag = True

    def slot_btn_show_network(self):
        for i in range(members.network_list.__len__()):
            plt.figure(members.network_list[i].graph['ID'])
            nx.draw(members.network_list[i], with_labels=True, font_weight='bold')
            plt.get_current_fig_manager().window.state('zoomed')
        plt.show()

    def save_scripts_to_xml(self):
        """
        保存脚本列表设置到xml文件中，保存成功为True，失败为False。
        :return:bool
        """
        # 设置保存路径，为本项目下的external_file文件夹
        save_path = "external_file"
        # 设置文件名
        file_name = "script.xml"
        # 保存表格中的内容
        doc = xml.dom.minidom.Document()
        SCRIPTS = doc.createElement('Scripts')
        doc.appendChild(SCRIPTS)
        for row in range(self.script_table_widget.rowCount()):
            SCRIPT = doc.createElement('Script')
            SCRIPT.setAttribute("id", str(row))
            for col in range(self.script_table_widget.columnCount()):
                # 在第一列，需要判断输入的迭代数是否合法
                if col == 0:
                    the_round = self.script_table_widget.item(row, col).text()
                    try:
                        # 需要判断一下在round列中的输入是不是int且不大于回合数设置
                        if int(the_round) < int(self.generation_Edit.text()):
                            SCRIPT.setAttribute("round", the_round)
                        else:
                            QtWidgets.QMessageBox.critical(self, "error",
                                                           "in row: {}\nOver generation.".format(str(row + 1)))
                            return False
                    except ValueError:
                        QtWidgets.QMessageBox.critical(self, "error",
                                                       "in row: {}\nRound number error.".format(str(row + 1)))
                        return False
                # 第二列，单纯保存一下名字就可以了
                elif col == 1:
                    the_name = self.script_table_widget.item(row, col).text()
                    SCRIPT.setAttribute("funcName", the_name)
                # 第三列，需要分离出文件名与文件所在路径
                elif col == 2:
                    the_path = self.script_table_widget.item(row, col).text()
                    module_name = the_path.split('/')[-1].split('.')[0]
                    SCRIPT.setAttribute("moduleName", module_name)
                    script_path = '/'.join(the_path.split('/')[0:-1])
                    SCRIPT.setAttribute("path", script_path)
                # 其他未知错误
                else:
                    QtWidgets.QMessageBox.critical(self, "error",
                                                   "in row: {}\nRound number error.".format(str(row + 1)))
            SCRIPTS.appendChild(SCRIPT)
        # 保存
        write_xml(save_path + '/' + file_name, doc)
        self.service_msg_log_text.append(str(datetime.now()) + ': ' + "Setting scripts succeed." + "({})".format(
            str(self.script_table_widget.rowCount())))
        return True

    def reset_member_tableWidget(self, length, id_role_dict):
        """
        重新设置成员表格信息
        :param length: 成员数
        :param id_role_dict: 成员信息字典
        :return:
        """
        self.member_tableWidget.setRowCount(length)
        item = self.member_tableWidget.horizontalHeaderItem(0)
        item.setText(QtCore.QCoreApplication.translate("Form", "Member"))
        item = self.member_tableWidget.horizontalHeaderItem(1)
        item.setText(QtCore.QCoreApplication.translate("Form", "Role"))
        self.member_tableWidget.setHorizontalHeaderItem(1, item)
        temp_arrow = 0
        for id, role in zip(id_role_dict['id'], id_role_dict['role']):
            id_item, role_item = QtWidgets.QTableWidgetItem(), QtWidgets.QTableWidgetItem()
            id_item.setText(QtCore.QCoreApplication.translate("Form", id))
            role_item.setText(QtCore.QCoreApplication.translate("Form", role))
            self.member_tableWidget.setItem(temp_arrow, 0, id_item)
            self.member_tableWidget.setItem(temp_arrow, 1, role_item)
            temp_arrow += 1

    def slot_btn_set_record_path(self):
        """
        设置仿真结果路径保存的槽函数
        :return: no return
        """
        dir_record_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择仿真记录文件夹", os.getcwd())
        if dir_record_path == "":
            self.service_msg_log_text.append(str(datetime.now()) + ': ' + 'Unselect record save path.')
        else:
            self.record_dir_path_edit.setText(dir_record_path)
            self.service_msg_log_text.append(
                str(datetime.now()) + ': ' + 'Set record dictionary to: ' + dir_record_path)
            # 需要初始化生成一个xml基础文件
            res = "<%s>""</%s>" % ("Result", "Result")
            record_dom = parseString(res)
            root = record_dom.getElementsByTagName("Result")[0]
            first_record_node = record_dom.createElement("Record")
            for v in external_func.global_attribute_dict.values():
                first_record_node.setAttribute(v['aName'], str(self.global_dict[v['aName']]))
            first_record_node.setAttribute("round", str(self.current_generation))
            root.appendChild(first_record_node)
            write_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml", record_dom)

    def start_check(self):
        if self.members_xml_path_edit.text() is "" or \
                self.def_xml_path_edit.text() is "" or \
                self.record_dir_path_edit.text() is "" or \
                self.version_edit.text() is "" or \
                self.step_size_Edit.text() is "" or \
                self.ex_ID_edit.text() is "" or \
                self.step_size_Edit.text() is "":
            return False
        else:
            record_dom = read_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml")
            record_dom_root = record_dom.getElementsByTagName("Result")[0]
            record_dom_root.setAttribute("ID", self.ex_ID_edit.text())
            record_dom_root.setAttribute("version", self.version_edit.text())
            record_dom_root.setAttribute("MetaMemberID", self.meta_member_ID_edit.text())
            record_dom_root.setAttribute("DefinitionID", self.definition_ID_edit.text())
            record_dom_root.setAttribute("RecordStepSize", self.step_size_Edit.text())
            record_dom_root.setAttribute("Inherited", str(eval(self.inherited_Edit.text())))
            record_dom_root.setAttribute("Datetime", self.modify_dateEdit.text())
            self.start_moment = datetime.now()
            record_dom_root.setAttribute("StartMoment", str(self.start_moment))
            write_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml", record_dom)
            return True

    def emit_round_method(self):
        if self.flag == "waiting" and self.start_check():
            self.flag = "running"
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.MyThread.flag = True
            save_member_round_record(self.record_dir_path_edit.text(),0,self.global_dict,len(self.generation_Edit.text()))
            self.MyThread.start()
            self.service_msg_log_text.append(str(self.start_moment) + ": Simulation task started.")

    def slot_test_button(self):
        # 任何可能用来测试的功能
        save_global_attribute_record(self.record_dir_path_edit.text(), 0, self.global_dict)
        pass

    def slot_terminate_simulation(self):
        # 加一步状态检测
        if self.flag == "running":
            # 加一步询问
            reply = QtWidgets.QMessageBox.question(self, "Terminate Simulation",
                                                   "Are you sure you want to teminate this simulation?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply:
                self.MyThread.terminate()
                self.end_moment = datetime.now()
                self.service_msg_log_text.append(str(self.end_moment) + ": Simulation task terminated.")
                record_dom = read_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml")
                record_dom_root = record_dom.getElementsByTagName("Result")[0]
                record_dom_root.setAttribute("EndMoment", str(self.end_moment))
                record_dom_root.setAttribute("TimeConsuming", str(self.end_moment - self.start_moment))
                write_xml(self.record_dir_path_edit.text() + "/Simulation_Record.xml", record_dom)
                self.current_generation = 0
                self.flag = "waiting"
                self.start_btn.setEnabled(True)
                self.pause_btn.setEnabled(False)
                self.MyThread.flag = False
                self.MyThread.current_generation = 0
                self.start_moment = None
                self.end_moment = None


def format_members_id_role(xml_dom: xml.dom.minidom.Document):
    """
    格式化成员的id与角色，本函数仅用于获取仿真成员xml文件中的部分简单信息包含成员id，成员角色，各类成员的数量
    :param xml_dom: xml文件的dom对象
    :return: key为id与role的dict，成员总个数，primitive成员的数量，collective成员的数量，adviser成员的数量，monitor成员的数量
    """
    root = xml_dom.documentElement  # 获取dom对象的根
    # 初始化id_role字典
    id_role_dict = {
        'id': list(),
        'role': list()
    }
    member_info_labels = root.getElementsByTagName('memberInfo')  # 获取memberInfo标签
    primitive_number = len(root.getElementsByTagName('primitiveInfo'))  # 获取primitiveInfo标签
    collective_number = len(root.getElementsByTagName('collectiveInfo'))  # 获取collectiveInfo标签
    adviser_number = len(root.getElementsByTagName('advisorInfo'))  # 获取advisorInfo标签
    monitorMember_number = len(root.getElementsByTagName('monitorMemberInfo'))  # 获取monitorMemberInfo标签
    for one_member_info_label in member_info_labels:
        id_role_dict['id'].append(one_member_info_label.getAttribute('成员ID'))
        id_role_dict['role'].append(one_member_info_label.getAttribute('成员类型'))
    return id_role_dict, len(
        member_info_labels), primitive_number, collective_number, adviser_number, monitorMember_number


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = uf_Form(globals())
    window.setWindowTitle('众智网络仿真执行工具软件')
    window.show()
    exit(app.exec_())
