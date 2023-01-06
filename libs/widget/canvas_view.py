# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-04 15:12:56
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-06 17:37:45
@FilePath: /labelp/libs/widget/canvas_view.py
@Description:
'''
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSceneMouseEvent
from PyQt5.QtCore import pyqtSignal, QPointF, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QKeyEvent, QPixmap, QCursor

from .shape import PointShape


class CanvasScene(QGraphicsScene):

    currentItemPosSignal = pyqtSignal(QPointF)
    currentItemInfoSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(CanvasScene, self).__init__(*args, **kwargs)
        self._isdrawing = False

    def mouseMoveEvent(self, event):  ##鼠标移动
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            if self._isdrawing:
                item = PointShape(len(self.items()))
                self.addItem(item)
                item.setPos(event.scenePos())
                self._isdrawing = False
                self.currentItemPosSignal.emit(event.scenePos())
                self.currentItemInfoSignal.emit("{}:{},{}".format(
                    item._label,
                    item.scenePos().x(),
                    item.scenePos().y()))
        super().mousePressEvent(event)


# class CanvasUtilsMixin(QGraphicsView):
# class CanvasUtilsMixin(object):
#     def cursorPos2Scene(self,cursorPos):
#         return self.mapToScene(self.mapFromGlobal(cursorPos))


class CanvasArea(QGraphicsView):
    stopDrawingSignal = pyqtSignal()

    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.backgroundPixmap = QPixmap()
        self.scene_ = CanvasScene(self)
        self.setScene(self.scene_)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)
        self.id = id
        self._ori_scale = 1

    @property
    def isdrawing(self):
        return self.scene_._isdrawing and (not self.backgroundPixmap.isNull())

    @isdrawing.setter
    def isdrawing(self, value: bool):
        self.scene_._isdrawing = (value
                                  and (not self.backgroundPixmap.isNull()))

    def scenePos2Cursor(self, scenePos):
        return self.mapToGlobal(self.mapFromScene(scenePos))

    def cursorPos2Scene(self, cursorPos):
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
        self.setSceneRect(*rect)
        # self.repaint()
        self.scene_.update(self.sceneRect())

    def prepareAddShape(self, scene_pos: QPointF):
        self.isdrawing = True
        QCursor.setPos(self.scenePos2Cursor(scene_pos))

    def paintEvent(self, pe):
        super().paintEvent(pe)

    def drawBackground(self, painter, rect):
        self.setSceneRect(-self.backgroundPixmap.width() / 2,
                          -self.backgroundPixmap.height() / 2,
                          self.backgroundPixmap.width(),
                          self.backgroundPixmap.height())
        painter.drawPixmap(self.sceneRect().left(),
                           self.sceneRect().top(), self.backgroundPixmap)
        self.scene_.setFocus()
        super().drawBackground(painter, rect)

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
            if 0.1 < self._ori_scale / s_v < 10:
                self.scale(s_v, s_v)
                self._ori_scale = self._ori_scale / s_v

            # self.centerOn(ev.globalPosition())
        #     self.zoomRequest.emit(v_delta)
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
        # print(self.id)
        if self.inImageRect(event.pos()):
            if self.isdrawing:
                self.setCursor(Qt.CrossCursor)
                #do samething
        else:
            pass
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):  ##鼠标单击
        self.setCursor(Qt.ArrowCursor)
        if event.button() == Qt.LeftButton:
            pass
            # if self.inImageRect(event.pos()):
            #     if self.isdrawing:
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):  ##鼠标双击
        if event.button() == Qt.LeftButton:
            point = event.pos()
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):  ##按键按下
        if event.key() == Qt.Key_Escape:
            self.stopDrawingSignal.emit()
            self.setCursor(Qt.ArrowCursor)
        super().keyPressEvent(event)
