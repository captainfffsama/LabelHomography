# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-05 12:56:36
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-12 16:41:21
@FilePath: /label_homography/libs/widget/shape/point_shape.py
@Description:
'''
from typing import Any
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QPainter, QBrush, QColor, QFocusEvent
from PyQt5.QtCore import QPointF, QRectF, Qt
from libs.config.color_list import get_color


class PointShape(QGraphicsItem):
    def __init__(self, label: int, shape_hash: str = None, *args, **kwargs):
        super(PointShape, self).__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self._label = label
        self._hash = shape_hash if shape_hash is not None else id(self)

    @property
    def hash(self):
        return str(self._hash)

    @property
    def belongScene(self):
        return self.scene().__class__.__name__

    def paint(self, painter: QPainter, option, widget):
        ori_pen = painter.pen()
        ori_brush = painter.brush()
        if self.isSelected():
            pen = QPen()
            pen.setColor(QColor("white"))
            pen.setWidth(3)
            brush = QBrush(QColor("indigo"), Qt.SolidPattern)
        else:
            pen = QPen()
            pen.setStyle(Qt.DotLine)
            pen.setWidth(2)
            pen.setColor(QColor("yellow"))
            brush = QBrush(get_color(self._label), Qt.SolidPattern)

        painter.setBrush(brush)
        painter.setPen(pen)

        painter.drawEllipse(self.boundingRect())

        painter.setPen(ori_pen)
        painter.setBrush(ori_brush)

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.isSelected():
            if not self.scene().sceneRect().contains(self.scenePos()):
                self.scene().delItemSignal.emit(self)

        return super().mouseReleaseEvent(event)

