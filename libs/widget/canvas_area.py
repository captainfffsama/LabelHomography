# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-19 17:29:06
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-03 15:55:25
@FilePath: /labelp/libs/widget/canvas_area.py
@Description:
'''

import sys
import os
from functools import lru_cache

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,QPointF
from PyQt5.QtGui import QPixmap,QPainter,QColor,QBrush

from .canvas import Canvas

class CanvasArea(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        self.canvas = Canvas()
        super().__init__(*args,**kwargs)
        self.canvas.zoomRequest.connect(self.zoomRequest)

        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidget(self.canvas)
        scrollArea.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: scrollArea.verticalScrollBar(),
            Qt.Horizontal: scrollArea.horizontalScrollBar(),
        }
        self.scroll_values = {
            Qt.Horizontal: {},
            Qt.Vertical: {},
        }  # key=filename, value=scroll_valueA
        self.canvas.scrollRequest.connect(self.scrollRequest)

        self.canvas.newShape.connect(self.newShape)
        self.canvas.shapeMoved.connect(self.setDirty)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

        self.pixmap=None
        self._painter = QPainter()
        self.scale = 1.0

    def offsetToCenter(self):
        s = self.scale
        area = super().size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPointF(x, y)

    def zoomRequest(self, delta, pos):
        canvas_width_old = self.canvas.width()
        units = 1.1
        if delta < 0:
            units = 0.9
        self.addZoom(units)

        canvas_width_new = self.canvas.width()
        if canvas_width_old != canvas_width_new:
            canvas_scale_factor = canvas_width_new / canvas_width_old

            x_shift = round(pos.x() * canvas_scale_factor) - pos.x()
            y_shift = round(pos.y() * canvas_scale_factor) - pos.y()

            self.setScroll(
                Qt.Horizontal,
                self.scrollBars[Qt.Horizontal].value() + x_shift,
            )
            self.setScroll(
                Qt.Vertical,
                self.scrollBars[Qt.Vertical].value() + y_shift,
            )

    def scrollRequest(self, delta, orientation):
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(value)
        self.scroll_values[orientation][self.filename] = value

    def newShape(self):
        pass
        # """Pop-up and give focus to the label editor.

        # position MUST be in global coordinates.
        # """
        # items = self.uniqLabelList.selectedItems()
        # text = None
        # if items:
        #     text = items[0].data(Qt.UserRole)
        # flags = {}
        # group_id = None
        # if self._config["display_label_popup"] or not text:
        #     previous_text = self.labelDialog.edit.text()
        #     text, flags, group_id = self.labelDialog.popUp(text)
        #     if not text:
        #         self.labelDialog.edit.setText(previous_text)

        # if text and not self.validateLabel(text):
        #     self.errorMessage(
        #         self.tr("Invalid label"),
        #         self.tr("Invalid label '{}' with validation type '{}'").format(
        #             text, self._config["validate_label"]
        #         ),
        #     )
        #     text = ""
        # if text:
        #     self.labelList.clearSelection()
        #     shape = self.canvas.setLastLabel(text, flags)
        #     shape.group_id = group_id
        #     self.addLabel(shape)
        #     self.actions.editMode.setEnabled(True)
        #     self.actions.undoLastPoint.setEnabled(False)
        #     self.actions.undo.setEnabled(True)
        #     self.setDirty()
        # else:
        #     self.canvas.undoLastLine()
        #     self.canvas.shapesBackups.pop()

    def setDirty(self):
        pass
        # # Even if we autosave the file, we keep the ability to undo
        # self.actions.undo.setEnabled(self.canvas.isShapeRestorable)

        # if self._config["auto_save"] or self.actions.saveAuto.isChecked():
        #     label_file = os.path.splitext(self.imagePath)[0] + ".json"
        #     if self.output_dir:
        #         label_file_without_path = os.path.basename(label_file)
        #         label_file = os.path.join(self.output_dir, label_file_without_path)
        #     self.saveLabels(label_file)
        #     return
        # self.dirty = True
        # self.actions.save.setEnabled(True)
        # title = "title_haha"
        # if self.filename is not None:
        #     title = "{} - {}*".format(title, self.filename)
        # self.setWindowTitle(title)

    def shapeSelectionChanged(self, selected_shapes):
        pass
        # self._noSelectionSlot = True
        # for shape in self.canvas.selectedShapes:
        #     shape.selected = False
        # self.labelList.clearSelection()
        # self.canvas.selectedShapes = selected_shapes
        # for shape in self.canvas.selectedShapes:
        #     shape.selected = True
        #     item = self.labelList.findItemByShape(shape)
        #     self.labelList.selectItem(item)
        #     self.labelList.scrollToItem(item)
        # self._noSelectionSlot = False
        # n_selected = len(selected_shapes)
        # self.actions.delete.setEnabled(n_selected)
        # self.actions.duplicate.setEnabled(n_selected)
        # self.actions.copy.setEnabled(n_selected)
        # self.actions.edit.setEnabled(n_selected == 1)

    def toggleDrawingSensitive(self, drawing=True):
        pass
        # """Toggle drawing sensitive.

        # In the middle of drawing, toggling between modes should be disabled.
        # """
        # self.actions.editMode.setEnabled(not drawing)
        # self.actions.undoLastPoint.setEnabled(drawing)
        # self.actions.undo.setEnabled(not drawing)
        # self.actions.delete.setEnabled(not drawing)

    @lru_cache(20)
    def loadPixmap(self, pixmap):
        self.pixmap = pixmap
        self.shapes = []
        self.update()

    def paintEvent(self, event):
        if not self.pixmap:
            return super().paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.scale(self.scale, self.scale)
        p.translate(self.offsetToCenter())

        p.drawPixmap(0, 0, self.pixmap)

        self.setAutoFillBackground(True)

        p.end()