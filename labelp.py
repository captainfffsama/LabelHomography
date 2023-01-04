# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-14 17:41:47
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-03 14:13:09
@FilePath: /labelp/labelp.py
@Description:
'''
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QTreeWidgetItem,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage,QPixmap

from libs.ui.ui_MainWindow import Ui_MainWindow
from libs.utils import get_sample_file,toQImage
from libs.widget.canvas_area import CanvasArea

SEPARATE_FLAG=" : "

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.statusbar.showMessage("握草", 5000)

        self.actionOpen_Dir.triggered.connect(self.show_file_dialog_slot)
        self.treeWidget.currentItemChanged.connect(self.tree_currentItemChanged_slot)

        draw_area_layout=QHBoxLayout(self.widget)
        self.tem_draw_area=CanvasArea(parent=self.widget)
        self.betest_draw_area=CanvasArea(parent=self.widget)
        draw_area_layout.addWidget(self.tem_draw_area)
        draw_area_layout.addWidget(self.betest_draw_area)

        self.data_dir=None

    def show_file_dialog_slot(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Open Dir", "./")
        if dir_path:
            self.data_dir=dir_path
            default_item=None
            self.samples_tree = get_sample_file(dir_path,filter=('.jpg','.JPG','.bmp','.BMP','.csv','.CSV'))
            self.treeWidget.clear()
            for k,v in self.samples_tree.items():
                root=QTreeWidgetItem(self.treeWidget)
                root.setText(0,os.path.basename(k)+SEPARATE_FLAG+os.path.basename(self.samples_tree[k]['t']))
                root.setFlags(root.flags()&~Qt.ItemIsSelectable)
                for i in self.samples_tree[k]['s']:
                    child=QTreeWidgetItem(root)
                    child.setText(0,os.path.basename(i))
                    if default_item is None:
                        default_item=child

                self.treeWidget.addTopLevelItem(root)
                if default_item is not None:
                    self.treeWidget.setCurrentItem(default_item)
            self.treeWidget.expandAll()
            print("get all file done!")
            print(self.samples_tree)

    def tree_currentItemChanged_slot(self,curren_item,previ_item):
        print("current changed")
        if curren_item is None:
            self.treeWidget.setCurrentItem(previ_item)
            return
        if curren_item.text(0).find(SEPARATE_FLAG) != -1:
            if previ_item !=self.treeWidget.itemBelow(curren_item):
                self.treeWidget.setCurrentItem(self.treeWidget.itemBelow(curren_item))
            else:
                self.treeWidget.setCurrentItem(self.treeWidget.itemAbove(curren_item))
        else:
            # 若当前文件是待标注文件
            current_t_path=os.path.join(self.data_dir,*curren_item.parent().text(0).split(SEPARATE_FLAG))
            current_b_path=os.path.join(self.data_dir,curren_item.parent().text(0).split(SEPARATE_FLAG)[0],curren_item.text(0))
            self.tem_draw_area.loadPixmap(QPixmap.fromImage(toQImage(current_t_path)))
            self.betest_draw_area.loadPixmap(QPixmap.fromImage(toQImage(current_b_path)))


    def scrollRequest(self, delta, orientation):
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(value)
        self.scroll_values[orientation][self.filename] = value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())