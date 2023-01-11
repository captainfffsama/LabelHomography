# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-04 15:12:56
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-11 10:44:49
@FilePath: /label_homography/libs/widget/canvas_view.py
@Description:
'''
from typing import Union
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsItem
from PyQt5.QtCore import pyqtSignal, QPointF, QPoint, Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QMouseEvent, QKeyEvent, QPixmap, QCursor

from libs.utils import QPointF2QPoint

from .shape import PointShape


def printqtrect(rect):
    print("rect:{},{},{},{}".format(rect.x(), rect.y(), rect.width(),
                                    rect.height()))


class CanvasSceneBase(QGraphicsScene):
    haveItemSelectedSignal = pyqtSignal()
    itemSelectedSignal = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs):
        super(CanvasSceneBase, self).__init__(*args, **kwargs)
        self._isdrawing = False

    def closeAllItemsSelected_slot(self):
        for item in self.items():
            item.setSelected(False)


class TemplateCanvasScene(CanvasSceneBase):
    itemDrawDoneSignal = pyqtSignal(QGraphicsItem)
    delItemSignal = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs):
        super(TemplateCanvasScene, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.sceneRect().contains(event.scenePos()):
            if event.button() == Qt.LeftButton:
                if self._isdrawing:
                    item = PointShape(len(self.items()))
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self._isdrawing = False
                    self.itemDrawDoneSignal.emit(item)
        return super().mousePressEvent(event)

    def add_points(self, points):
        for idx, ps in enumerate(points):
            item = PointShape(idx, str(idx))
            self.addItem(item)
            pos = QPoint(ps[0] + self.sceneRect().topLeft().x(),
                         ps[1] + self.sceneRect().topLeft().y())
            item.setPos(pos)
        self._isdrawing = False


class SampleCanvasScene(CanvasSceneBase):
    itemDrawDoneSignal = pyqtSignal(QGraphicsItem)
    delItemSignal = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs):
        super(SampleCanvasScene, self).__init__(*args, **kwargs)
        self._needAddShapes = []

    def prepareAddShape_slot(self, shape):
        self._needAddShapes.append(PointShape(shape._label, shape.hash))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.sceneRect().contains(event.scenePos()):
            if event.button() == Qt.LeftButton:
                if self._isdrawing and self._needAddShapes:
                    item = self._needAddShapes.pop()
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self._isdrawing = False
                    self.itemDrawDoneSignal.emit(item)
        return super().mousePressEvent(event)

    def add_points(self, points):
        for idx, ps in enumerate(points):
            item = PointShape(idx, str(idx))
            self.addItem(item)
            pos = QPoint(ps[0] + self.sceneRect().topLeft().x(),
                         ps[1] + self.sceneRect().topLeft().y())
            item.setPos(pos)
        self._isdrawing = False


class CanvasView(QGraphicsView):
    stopDrawingSignal = pyqtSignal()

    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.backgroundPixmap = QPixmap()
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)
        self.id = id

    @property
    def isdrawing(self):
        return self.scene()._isdrawing and (not self.backgroundPixmap.isNull())

    @isdrawing.setter
    def isdrawing(self, value: bool):
        self.scene()._isdrawing = (value
                                   and (not self.backgroundPixmap.isNull()))

    def scenePos2Cursor(self, scenePos):
        if isinstance(scenePos, QPointF):
            scenePos = QPointF2QPoint(scenePos)
        return self.mapToGlobal(self.mapFromScene(scenePos))

    def cursorPos2Scene(self, cursorPos):
        if isinstance(cursorPos, QPointF):
            cursorPos = QPointF2QPoint(cursorPos)
        return self.mapToScene(self.mapFromGlobal(cursorPos))

    @property
    def center_global_pos(self):
        return self.cursorPos2Scene(QPointF(0, 0))

    def inImageRect(self, viewPos):
        return self.mapFromScene(
            self.sceneRect()).boundingRect().contains(viewPos)

    def loadPixmap(self, pixmap):
        self.backgroundPixmap = pixmap
        rect = (-self.backgroundPixmap.width() / 2,
                -self.backgroundPixmap.height() / 2,
                self.backgroundPixmap.width(), self.backgroundPixmap.height())
        self.scene().setSceneRect(*rect)
        self.fitInView(*rect, Qt.KeepAspectRatio)

        self.scene().update(self.sceneRect())

    def prepareAddShape(self, scene_pos: Union[QPointF, QPoint,
                                               QGraphicsItem]):
        self.startDrawing()
        if isinstance(scene_pos, QGraphicsItem):
            scene_pos = scene_pos.scenePos()
        self.centerOn(scene_pos)
        QCursor.setPos(self.scenePos2Cursor(scene_pos))

    def drawBackground(self, painter, rect):
        self.scene().setSceneRect(-self.backgroundPixmap.width() / 2,
                                  -self.backgroundPixmap.height() / 2,
                                  self.backgroundPixmap.width(),
                                  self.backgroundPixmap.height())
        painter.drawPixmap(self.sceneRect().left(),
                           self.sceneRect().top(), self.backgroundPixmap)
        return super().drawBackground(painter, rect)

    def wheelEvent(self, ev):
        delta = ev.angleDelta()
        h_delta = delta.x()
        v_delta = delta.y()

        mods = ev.modifiers()
        if Qt.ControlModifier == int(mods):
            if v_delta:
                s_v = 1 + v_delta / abs(v_delta) * 0.1
            else:
                s_v = 1
            if 0.01 < self.transform().m11() < 20:
                self.scale(s_v, s_v)

            self.centerOn(
                self.cursorPos2Scene(QPointF2QPoint(ev.globalPosition())))
        else:
            if v_delta:
                c = int((self.verticalScrollBar().maximum() -
                         self.verticalScrollBar().minimum()) * 0.1)
                v = self.verticalScrollBar().value(
                ) - c if v_delta < 0 else self.verticalScrollBar().value() + c
                v = max(self.verticalScrollBar().minimum(), v)
                v = min(self.verticalScrollBar().maximum(), v)
                self.verticalScrollBar().setValue(v)
            if h_delta:
                c = int((self.horizontalScrollBar().maximum() -
                         self.horizontalScrollBar().minimum()) * 0.1)
                v = self.horizontalScrollBar().value(
                ) - c if v_delta < 0 else self.horizontalScrollBar().value(
                ) + c
                v = max(self.horizontalScrollBar().minimum(), v)
                v = min(self.horizontalScrollBar().maximum(), v)
                self.horizontalScrollBar().setValue(v)
        ev.accept()

    def mouseMoveEvent(self, event):  ##鼠标移动
        point = event.pos()
        if self.inImageRect(event.pos()):
            if self.isdrawing:
                self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):  ##鼠标单击
        if event.button() == Qt.MiddleButton:
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        return super().mousePressEvent(event)

    def keyPressEvent(self, event):  ##按键按下
        if event.key() == Qt.Key_Escape:
            self.stopDrawingSignal.emit()

        return super().keyPressEvent(event)

    def startDrawing(self):
        self.setCursor(Qt.CrossCursor)
        self.isdrawing = True
        for item in self.scene().items():
            item.setFlags(QGraphicsItem.ItemIgnoresTransformations)

    def stopDrawing(self):
        self.setCursor(Qt.ArrowCursor)
        self.isdrawing = False
        for item in self.scene().items():
            item.setFlags(QGraphicsItem.ItemIgnoresTransformations
                          | QGraphicsItem.ItemIsMovable
                          | QGraphicsItem.ItemIsSelectable)
