# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-09 17:01:01
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-12 15:55:50
@FilePath: /label_homography/libs/widget/label_list_widget.py
@Description:
'''

import weakref
from PyQt5.QtWidgets import QListWidget,QGraphicsItem,QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal

from libs.widget.label_list_item import LabelItemWidget
from libs.utils import printFuncName


class LabelListWidget(QListWidget):
    needDelItem = pyqtSignal(str)
    currentItemTypeSignal = pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(LabelListWidget, self).__init__(*args, **kwargs)
        self.currentItemChanged.connect(self.currentItemChanged_slot)
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self._itemMap=weakref.WeakValueDictionary()

    def addItem(self, item):
        if getattr(item, 'hash'):
            self._itemMap[item.hash] = item
        return super().addItem(item)

    def clear(self):
        self._itemMap.clear()
        return super().clear()

    def findItemByHash(self, hash):
        return self._itemMap.get(hash, None)

    def takeItemByHash(self, hash):
        item = self.findItemByHash(hash)
        if item:
            self._itemMap.pop(hash,None)
            self.takeItem(self.row(item))

    def insertItem(self, item):
        if getattr(item, 'hash'):
            self._itemMap[item.hash] = item
        return super().insertItem(item)

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete:
            if self.currentItem():
                self.needDelItem.emit(self.currentItem().hash)
        return super().keyReleaseEvent(event)

    def selectionChanged(self,selected,deselected):
        print("label list selected item:",self.selectedItems()[0].hash)
        print("current item:",self.currentItem().hash)
        super().selectionChanged(selected,deselected)

    # @printFuncName
    def currentItemChanged_slot(self, current, previous):
        if previous:
            self.removeItemWidget(previous)
            print("p:",previous._label)
        if current is not None:
            print("c:",current._label)
            self.setCurrentItem(current)
            itemWidget = LabelItemWidget()
            self.setItemWidget(current, itemWidget)
            itemWidget.currentItemTypeSignal.connect(self.getCurrentItemTypeSlot)
            itemWidget.currentItemType_slot()

    def getCurrentItemTypeSlot(self, item_type):
        if self.currentItem():
            self.currentItemTypeSignal.emit(self.currentItem().hash, item_type)

    def setItemSelectedFromGraphicsItemSlot(self, gitem:QGraphicsItem):
        item=self.findItemByHash(gitem.hash)
        if item != self.currentItem():
            self.setCurrentItem(item)
            # item.setSelected(True)
            label_item_widget = self.itemWidget(item)
            if label_item_widget:
                if gitem.belongScene == "TemplateCanvasScene":
                    label_item_widget.templateBtn.setChecked(True)
                elif gitem.belongScene == "SampleCanvasScene":
                    label_item_widget.sampleBtn.setChecked(True)
                else:
                    pass

    def clearCurrentItemWidget(self) -> None:
        self.removeItemWidget(self.currentItem())
        self.setCurrentItem(None)
