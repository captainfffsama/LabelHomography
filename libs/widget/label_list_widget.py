# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-09 17:01:01
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-11 15:29:18
@FilePath: /label_homography/libs/widget/label_list_widget.py
@Description:
'''

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt, pyqtSignal

from libs.widget.label_list_item import LabelItemWidget


class LabelListWidget(QListWidget):
    needDelItem = pyqtSignal(str)
    currentItemTypeSignal = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(LabelListWidget, self).__init__(*args, **kwargs)
        self.currentItemChanged.connect(self.currentItemChanged_slot)
        self.setSortingEnabled(True)

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete:
            if self.currentItem():
                self.needDelItem.emit(self.currentItem().hash)
        return super().keyReleaseEvent(event)

    def currentItemChanged_slot(self, current, previous):
        self.removeItemWidget(previous)
        itemWidget = LabelItemWidget()
        self.setItemWidget(current, itemWidget)

        itemWidget.currentItemTypeSignal.connect(self.getCurrentItemTypeSlot)
        itemWidget.currentItemType_slot()

    def getCurrentItemTypeSlot(self, item_type):
        if self.currentItem():
            self.currentItemTypeSignal.emit(self.currentItem().hash, item_type)

    def setItemSelectedFromGraphicsItemSlot(self, gitem):
        for item in self.findItems(str(gitem._label), Qt.MatchExactly):
            if item.hash == gitem.hash:
                self.setCurrentItem(item)
            label_item_widget = self.itemWidget(item)
        if label_item_widget:
            if gitem.belongScene == "TemplateCanvasScene":
                label_item_widget.templateBtn.setChecked(True)
            elif gitem.belongScene == "SampleCanvasScene":
                label_item_widget.sampleBtn.setChecked(True)
            else:
                pass
