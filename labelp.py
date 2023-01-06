# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-14 17:41:47
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-06 17:41:17
@FilePath: /labelp/labelp.py
@Description:
'''
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QHBoxLayout, QVBoxLayout,QActionGroup
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QImage, QPixmap,QCursor

from libs.ui.ui_MainWindow import Ui_MainWindow
from libs.utils import get_sample_file, toQImage
from libs.widget.canvas_view import CanvasArea

SEPARATE_FLAG = " : "


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.statusbar.showMessage("握草", 5000)

        self.actionAddShapeGroup=QActionGroup(self)
        self.actionAddShapeGroup.addAction(self.actionPoint_Shape)

        self.actionOpenDir.triggered.connect(self.show_file_dialog_slot)
        self.actionPreviousSample.triggered.connect(self.previous_sample_select_slot)
        self.actionNextSample.triggered.connect(self.next_sample_select_slot)
        self.actionAddShape.triggered.connect(self.actionAddShape_triggered_slot)


        self.treeWidget.currentItemChanged.connect(
            self.tree_currentItemChanged_slot)

        draw_area_layout = QVBoxLayout(self.widget)
        self.tem_draw_area = CanvasArea(id="tem",parent=self.widget)
        self.betest_draw_area = CanvasArea(id="be",parent=self.widget)
        draw_area_layout.addWidget(self.tem_draw_area)
        draw_area_layout.addWidget(self.betest_draw_area)

        self.tem_draw_area.scene_.currentItemPosSignal.connect(self.betest_draw_area.prepareAddShape)
        self.betest_draw_area.scene_.currentItemPosSignal.connect(self.tem_draw_area.prepareAddShape)

        self.data_dir = None

    def actionAddShape_triggered_slot(self):
        self.tem_draw_area.prepareAddShape(QPoint(0,0))

    def stopAddItemSlot(self):
        self.tem_draw_area.items()

    def show_file_dialog_slot(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Open Dir", "./")
        if dir_path:
            self.data_dir = dir_path
            default_item = None
            self.samples_tree = get_sample_file(dir_path,
                                                filter=('.jpg', '.JPG', '.bmp',
                                                        '.BMP', '.csv',
                                                        '.CSV'))
            self.treeWidget.clear()
            for k, v in self.samples_tree.items():
                root = QTreeWidgetItem(self.treeWidget)
                root.setText(
                    0,
                    os.path.basename(k) + SEPARATE_FLAG +
                    os.path.basename(self.samples_tree[k]['t']))
                root.setFlags(root.flags() & ~Qt.ItemIsSelectable)
                for i in self.samples_tree[k]['s']:
                    child = QTreeWidgetItem(root)
                    child.setText(0, os.path.basename(i))
                    if default_item is None:
                        default_item = child

                self.treeWidget.addTopLevelItem(root)
                if default_item is not None:
                    self.treeWidget.setCurrentItem(default_item)
            self.treeWidget.expandAll()
            print("get all file done!")
            print(self.samples_tree)

    def previous_sample_select_slot(self):
        print("aaa")
        self.treeWidget.setCurrentItem(
            self.treeWidget.itemAbove(self.treeWidget.currentItem()))

    def next_sample_select_slot(self):
        print("nnn")
        self.treeWidget.setCurrentItem(
            self.treeWidget.itemBelow(self.treeWidget.currentItem()))

    def tree_currentItemChanged_slot(self, curren_item, previ_item):
        if curren_item is None:
            self.treeWidget.setCurrentItem(previ_item)
            return
        if curren_item.text(0).find(SEPARATE_FLAG) != -1:
            if previ_item != self.treeWidget.itemBelow(curren_item):
                self.treeWidget.setCurrentItem(
                    self.treeWidget.itemBelow(curren_item))
            else:
                self.treeWidget.setCurrentItem(
                    self.treeWidget.itemAbove(curren_item))
        else:
            # 若当前文件是待标注文件
            print("current changed")
            print(curren_item.text(0))
            current_t_path = os.path.join(
                self.data_dir,
                *curren_item.parent().text(0).split(SEPARATE_FLAG))
            current_b_path = os.path.join(
                self.data_dir,
                curren_item.parent().text(0).split(SEPARATE_FLAG)[0],
                curren_item.text(0))
            self.tem_draw_area.loadPixmap(
                QPixmap.fromImage(toQImage(current_t_path)))
            self.betest_draw_area.loadPixmap(
                QPixmap.fromImage(toQImage(current_b_path)))


    def mouseMoveEvent(self, event):
        self.setFocus()
        print("======")
        print(self.tem_draw_area.hasFocus())
        print(self.tem_draw_area.focusPolicy())
        super().mouseMoveEvent(event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())