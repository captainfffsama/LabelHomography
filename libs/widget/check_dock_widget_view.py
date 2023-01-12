# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-01-11 12:41:44
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-12 16:01:23
@FilePath: /label_homography/libs/widget/check_dock_widget_view.py
@Description:
'''

from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QFrame
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap
from libs.utils import QPointF2QPoint, ndarray2QTransform, printQTransform


class CheckDockWidgetCanvasView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.backgroundPixmap = QPixmap()
        self.setFocusPolicy(Qt.WheelFocus)
        self.setFrameShape(QFrame.NoFrame)

    def inImageRect(self, viewPos):
        return self.mapFromScene(
            self.sceneRect()).boundingRect().contains(viewPos)

    def cursorPos2Scene(self, cursorPos):
        if isinstance(cursorPos, QPointF):
            cursorPos = QPointF2QPoint(cursorPos)
        return self.mapToScene(self.mapFromGlobal(cursorPos))

    def loadPixmap(self, pixmap):
        self.backgroundPixmap = pixmap
        rect = (-self.backgroundPixmap.width() / 2,
                -self.backgroundPixmap.height() / 2,
                self.backgroundPixmap.width(), self.backgroundPixmap.height())
        self.scene().setSceneRect(*rect)
        self.fitInView(*rect, Qt.KeepAspectRatio)

        self.scene().update(self.sceneRect())

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
            self.centerOn(
                self.cursorPos2Scene(QPointF2QPoint(ev.globalPosition())))
            if v_delta:
                s_v = 1 + v_delta / abs(v_delta) * 0.1
            else:
                s_v = 1
            self.scale(s_v, s_v)

        else:
            if v_delta:
                c = int((self.verticalScrollBar().maximum() -
                         self.verticalScrollBar().minimum()) * 0.1)
                v = self.verticalScrollBar().value(
                ) - c if v_delta > 0 else self.verticalScrollBar().value() + c
                v = max(self.verticalScrollBar().minimum(), v)
                v = min(self.verticalScrollBar().maximum(), v)
                self.verticalScrollBar().setValue(v)
            if h_delta:
                c = int((self.horizontalScrollBar().maximum() -
                         self.horizontalScrollBar().minimum()) * 0.1)
                v = self.horizontalScrollBar().value(
                ) - c if h_delta > 0 else self.horizontalScrollBar().value(
                ) + c
                v = max(self.horizontalScrollBar().minimum(), v)
                v = min(self.horizontalScrollBar().maximum(), v)
                self.horizontalScrollBar().setValue(v)
        ev.accept()

    def mousePressEvent(self, event):  ##鼠标单击
        if event.button() == Qt.MiddleButton:
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        return super().mousePressEvent(event)

    def showFinalImage(self, timg, simg, H):
        self.scene().clear()
        template_qpixmap = QPixmap.fromImage(timg)
        template_qgitem = QGraphicsPixmapItem(template_qpixmap)
        template_qgitem.setOpacity(0.5)

        sample_qpixmap = QPixmap.fromImage(simg)
        sample_qgitem = QGraphicsPixmapItem(sample_qpixmap)
        sample_qgitem.setOpacity(0.5)
        sample_qgitem.setTransform(ndarray2QTransform(H), combine=True)

        self.scene().addItem(sample_qgitem)
        self.scene().addItem(template_qgitem)