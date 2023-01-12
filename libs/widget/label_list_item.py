# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-09 16:23:28
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-12 15:15:54
@FilePath: /label_homography/libs/widget/label_list_item.py
@Description:
'''
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QRadioButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QColor

from libs.config.color_list import get_color


class LabelItemWidget(QWidget):
    currentItemTypeSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(LabelItemWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.label = QLabel()
        self.templateBtn = QRadioButton("Template")
        self.templateBtn.setChecked(True)
        self.sampleBtn = QRadioButton("Sample")
        layout.addWidget(self.label)
        layout.addWidget(self.templateBtn)
        layout.addWidget(self.sampleBtn)
        self.setLayout(layout)

        self.templateBtn.toggled.connect(self.currentItemType_slot)
        self.sampleBtn.toggled.connect(self.currentItemType_slot)

    def currentItemType_slot(self):
        if self.templateBtn.isChecked():
            self.currentItemTypeSignal.emit("Template")
        else:
            self.currentItemTypeSignal.emit("Sample")


class LabelListItem(QListWidgetItem):
    def __init__(self, text="", hash=None, *args, **kwargs):
        super(LabelListItem, self).__init__(*args, **kwargs)
        self.setText(text)
        self._label = text
        self._hash = hash if hash is not None else id(self)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setBackground(get_color(int(text)))
        self.setSizeHint(QSize(0, 35))
        # self.setData(Qt.DisplayRole,self._label+":"+self._hash)

    @property
    def hash(self):
        return str(self._hash)
