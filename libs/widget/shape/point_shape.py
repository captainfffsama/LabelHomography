# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-05 12:56:36
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-06 16:01:10
@FilePath: /labelp/libs/widget/shape/point_shape.py
@Description:
'''
from PyQt5.QtWidgets import QGraphicsItem,QGraphicsEllipseItem
from PyQt5.QtGui import QPen,QPainter,QBrush,QColor
from PyQt5.QtCore import QPointF,QRectF,Qt
from libs.config.color_list import COLOR_LIST
# class PointShape(QGraphicsEllipseItem):
#     def __init__(self,label:int,cursorpos:QPointF,*args,**kwargs):
#         super(PointShape, self).__init__(*args,**kwargs)
#         # self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
#         self._label=label
#         self._pos=cursorpos
#         print("=============")
#         print(self._pos)
#         print(self.pos().x(),self.pos().y())
#         print(self.scenePos().x(),self.scenePos().y())


class PointShape(QGraphicsItem):
    def __init__(self,label:int,*args,**kwargs):
        super(PointShape, self).__init__(*args,**kwargs)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self._label=label

    def paint(self,painter:QPainter, option,widget):
        ori_pen=painter.pen()
        ori_brush=painter.brush()

        pen=QPen()
        pen.setColor(QColor(*COLOR_LIST[self._label]))

        brush=QBrush(QColor(*COLOR_LIST[self._label]),Qt.SolidPattern)

        painter.setBrush(brush)
        painter.setPen(pen)

        # painter.drawPoint(QPoint(100,100))
        painter.drawEllipse(self.boundingRect())

        painter.setPen(ori_pen)
        painter.setBrush(ori_brush)

    def boundingRect(self):
        return QRectF(-3,-3,6,6)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super().mouseMoveEvent(event)




