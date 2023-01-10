# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-09 17:01:01
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-10 10:06:32
@FilePath: /labelp/libs/widget/label_list_widget.py
@Description:
'''

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt,pyqtSignal

from libs.widget.label_list_item import LabelItemWidget

class LabelListWidget(QListWidget):
    needDelItem=pyqtSignal(str)
    currentItemTypeSignal=pyqtSignal(str,str)

    def __init__(self, *args, **kwargs):
        super(LabelListWidget, self).__init__(*args, **kwargs)
        self.currentItemChanged.connect(self.currentItemChanged_slot)

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete:
            if self.currentItem():
                self.needDelItem.emit(self.currentItem().hash)
        super().keyReleaseEvent(event)

    def currentItemChanged_slot(self,current,previous):
        print("run")
        self.removeItemWidget(previous)
        itemWidget=LabelItemWidget()
        self.setItemWidget(current,itemWidget)

        itemWidget.currentItemTypeSignal.connect(self.getCurrentItemTypeSlot)
        itemWidget.currentItemType_slot()

    def getCurrentItemTypeSlot(self,item_type):
        if self.currentItem():
            self.currentItemTypeSignal.emit(self.currentItem().hash,item_type)