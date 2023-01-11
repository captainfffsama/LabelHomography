# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-14 17:41:47
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-11 15:38:29
@FilePath: /label_homography/app.py
@Description:
'''
import json
from collections import defaultdict
import sys
import os

import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QVBoxLayout, QActionGroup, QGraphicsItem,QGraphicsScene, QMessageBox,QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPoint, QSize, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap, QCursor, QColor

from libs.ui.ui_MainWindow import Ui_MainWindow
from libs.utils import get_sample_file, toQImage, countH
from libs.widget.canvas_view import CanvasView, TemplateCanvasScene, SampleCanvasScene
from libs.widget.check_dock_widget_view import CheckDockWidgetCanvasView
from libs.widget.label_list_item import LabelListItem, LabelItemWidget
from libs.widget.label_list_widget import LabelListWidget
import apprcc_rc

SEPARATE_FLAG = " : "


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.fixUI()

        self._tr = QCoreApplication.translate

        self.actionAddShapeGroup = QActionGroup(self)
        self.actionAddShapeGroup.addAction(self.actionPoint_Shape)

        self.actionOpenDir.triggered.connect(self.show_file_dialog_slot)
        self.actionPreviousSample.triggered.connect(
            self.previousSampleSelectSlot)
        self.actionNextSample.triggered.connect(self.nextSampleSelectSlot)
        self.actionAddShape.triggered.connect(
            self.actionAddShape_triggered_slot)
        self.actionSave.triggered.connect(self.saveLabelFileSlot)

        self.dataListWidget.currentItemChanged.connect(
            self.treeCurrentItemChangedSlot)

        draw_area_layout = QVBoxLayout(self.widget)
        self.tem_draw_area = CanvasView(id="tem", parent=self.widget)
        self.tem_draw_scene = TemplateCanvasScene()
        self.tem_draw_area.setScene(self.tem_draw_scene)
        self.sample_draw_area = CanvasView(id="be", parent=self.widget)
        self.sample_draw_scene = SampleCanvasScene()
        self.sample_draw_area.setScene(self.sample_draw_scene)
        draw_area_layout.addWidget(self.tem_draw_area)
        draw_area_layout.addWidget(self.sample_draw_area)

        self.tem_draw_area.scene().itemDrawDoneSignal.connect(
            self.sample_draw_area.prepareAddShape)
        self.tem_draw_area.scene().itemDrawDoneSignal.connect(
            self.sample_draw_area.scene().prepareAddShape_slot)
        self.tem_draw_area.scene().delItemSignal.connect(self.delItemSlot)
        self.tem_draw_area.scene().haveItemSelectedSignal.connect(
            self.sample_draw_area.scene().closeAllItemsSelected_slot)
        self.tem_draw_area.scene().itemSelectedSignal.connect(
            self.labelListWidget.setItemSelectedFromGraphicsItemSlot)

        self.sample_draw_area.scene().itemDrawDoneSignal.connect(
            self.shapePairdrawDone_slot)
        self.sample_draw_area.scene().delItemSignal.connect(self.delItemSlot)
        self.sample_draw_area.scene().haveItemSelectedSignal.connect(
            self.tem_draw_area.scene().closeAllItemsSelected_slot)
        self.sample_draw_area.scene().itemSelectedSignal.connect(
            self.labelListWidget.setItemSelectedFromGraphicsItemSlot)

        self.tem_draw_area.stopDrawingSignal.connect(self.stopAddItemSlot)
        self.sample_draw_area.stopDrawingSignal.connect(self.stopAddItemSlot)

        self.data_dir = None
        self.current_t_path = None
        self.current_t_qimage= None
        self.current_s_path = None
        self.current_t_qimage= None

        self.shapes_info = defaultdict(dict)

    def fixUI(self):
        self.horizontalLayout_3.removeWidget(self.labelListWidget)
        self.labelListWidget = LabelListWidget(self.dockWidgetContents_4)
        self.labelListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontalLayout_3.addWidget(self.labelListWidget)
        self.labelListWidget.needDelItem.connect(self.delItemSlot)
        self.labelListWidget.currentItemTypeSignal.connect(
            self.showSelectShape)

        self.menuView.addAction(self.dockWidget_label.toggleViewAction())
        self.menuView.addAction(self.dockWidget_file.toggleViewAction())
        self.menuView.addAction(self.dockWidget_check.toggleViewAction())

        self.checkDockWidgetView=CheckDockWidgetCanvasView(self.dockWidget_check)
        self.checkDockWidgetView.setScene(QGraphicsScene(self.checkDockWidgetView))
        self.horizontalLayout_4.addWidget(self.checkDockWidgetView)

    def showSelectShape(self, shape_id, shape_type):
        self.tem_draw_area.scene().update()
        self.sample_draw_area.scene().update()
        self.stopAddItemSlot()
        if shape_type == "Template":
            view=self.tem_draw_area
            for item in self.sample_draw_area.scene().items():
                item.setSelected(False)
        else:

            view=self.sample_draw_area
            for item in self.tem_draw_area.scene().items():
                item.setSelected(False)

        for item in view.scene().items():
            if item.hash == shape_id:
                item.setSelected(True)
                view.centerOn(item.scenePos())
            else:
                item.setSelected(False)

    def actionAddShape_triggered_slot(self):
        self.tem_draw_area.prepareAddShape(QPoint(0, 0))

    def shapePairdrawDone_slot(self, shape: QGraphicsItem):
        self.actionAddShape_triggered_slot()

        listItem = LabelListItem(text=str(shape._label),
                                 hash=shape.hash,
                                 parent=self.labelListWidget)
        self.labelListWidget.addItem(listItem)
        self.shapes_info[shape.hash]['SampleShape'] = shape
        self.shapes_info[shape.hash]['ListItem'] = listItem
        for idx, item in enumerate(self.tem_draw_area.scene().items()):
            if item.hash == shape.hash:
                self.shapes_info[shape.hash][
                    'TemplateShape'] = self.tem_draw_area.scene().items()[idx]

    def delItemSlot(self, item_hash):
        if isinstance(item_hash, QGraphicsItem):
            item_hash = item_hash.hash
        if item_hash in self.shapes_info:
            delShapes_info = self.shapes_info.pop(item_hash)
            self.labelListWidget.takeItem(
                self.labelListWidget.row(delShapes_info['ListItem']))
            self.sample_draw_area.scene().removeItem(
                delShapes_info['SampleShape'])
            self.tem_draw_area.scene().removeItem(
                delShapes_info['TemplateShape'])
        else:
            for item_row in range(self.labelListWidget.count()):
                if self.labelListWidget.item(item_row).hash == item_hash:
                    self.labelListWidget.takeItem(item_row)
            for item in self.sample_draw_area.scene().items():
                if item.hash == item_hash:
                    self.sample_draw_area.scene().removeItem(item)

            for item in self.tem_draw_area.scene().items():
                if item.hash == item_hash:
                    self.tem_draw_area.scene().removeItem(item)

    def saveLabelFileSlot(self):
        if self.current_t_path and self.current_s_path:
            self.stopAddItemSlot()
            template_ps = []
            sample_ps = []
            t_scene_rect = self.tem_draw_area.sceneRect()
            s_scene_rect = self.sample_draw_area.sceneRect()
            final_result = {}
            for k, v in self.shapes_info.items():
                tps = v['TemplateShape'].scenePos() - t_scene_rect.topLeft()
                sps = v['SampleShape'].scenePos() - s_scene_rect.topLeft()
                template_ps.append((tps.x(), tps.y()))
                sample_ps.append((sps.x(), sps.y()))

            template_info = {}
            template_info['Path'] = self.current_t_path
            template_info['ImageSize'] = (int(t_scene_rect.width()),
                                          int(t_scene_rect.height()))
            template_info['Points'] = template_ps

            sample_info = {}
            sample_info['Path'] = self.current_s_path
            sample_info['ImageSize'] = (int(s_scene_rect.width()),
                                        int(s_scene_rect.height()))
            sample_info['Points'] = sample_ps

            final_result["Template"] = template_info
            final_result["Sample"] = sample_info
            if not sample_ps:
                return

            #count H
            H,mask = countH(sample_ps, template_ps)
            print(mask)
            if H is not None:
                final_result["Sample2Template Matrix"] = H.tolist()
                self.checkDockWidgetView.showFinalImage(self.current_t_qimage,self.current_s_qimage,H.T)
            else:
                title = self._tr(self.__class__.__name__, "Error")
                text = self._tr(
                    self.__class__.__name__,
                    "Opencv count sample to template homography matrix failed! \
                    \n May be points labeled no good enough.Please do not label all points in one line! \
                    \n All label points will be removed!This label wont be saved!"
                )
                QMessageBox.critical(self, title, text, QMessageBox.Yes,
                                     QMessageBox.Yes)

                self.statusbar.showMessage(
                    "{} H count failed!".format(
                        os.path.basename(self.current_s_path)), 5000)
                self.cleanShape()
                return

            sample_name, ext = os.path.splitext(self.current_s_path)
            with open(sample_name + '.json', 'w') as f:
                json.dump(final_result, f, indent=4, ensure_ascii=False)

            self.statusbar.showMessage(
                "{} label save done".format(
                    os.path.basename(self.current_s_path)), 5000)

    def stopAddItemSlot(self):
        for item in self.tem_draw_area.scene().items():
            if item.hash not in self.shapes_info:
                self.tem_draw_area.scene().removeItem(item)

        self.tem_draw_area.stopDrawing()
        self.sample_draw_area.stopDrawing()

    def show_file_dialog_slot(self):
        self.dataListWidget.clear()
        dir_path = QFileDialog.getExistingDirectory(self, "Open Dir", "./")
        if dir_path:
            self.data_dir = dir_path
            default_item = None
            samples_tree = get_sample_file(dir_path,
                                           filter=('.jpg', '.JPG', '.png',
                                                   '.PNG', '.bmp', '.BMP',
                                                   '.csv', '.CSV'))
            self.dataListWidget.clear()
            for k, v in samples_tree.items():
                root = QTreeWidgetItem(self.dataListWidget)
                root.setText(
                    0,
                    os.path.basename(k) + SEPARATE_FLAG +
                    os.path.basename(samples_tree[k]['t']))
                root.setFlags(root.flags() & ~Qt.ItemIsSelectable)
                for i in samples_tree[k]['s']:
                    child = QTreeWidgetItem(root)
                    child.setText(0, os.path.basename(i))
                    if default_item is None:
                        default_item = child

                self.dataListWidget.addTopLevelItem(root)
                if default_item is not None:
                    self.dataListWidget.setCurrentItem(default_item)
            self.dataListWidget.expandAll()
            print("get all file done!")

    def previousSampleSelectSlot(self):
        if self.actionAuto_Save.isChecked():
            self.saveLabelFileSlot()
        self.stopAddItemSlot()
        self.cleanShape()
        self.dataListWidget.setCurrentItem(
            self.dataListWidget.itemAbove(self.dataListWidget.currentItem()))

    def cleanShape(self):
        self.tem_draw_area.scene().clear()
        self.sample_draw_area.scene().clear()
        self.shapes_info.clear()
        self.labelListWidget.clear()
        self.checkDockWidgetView.scene().clear()

    def nextSampleSelectSlot(self):
        if self.actionAuto_Save.isChecked():
            self.saveLabelFileSlot()
        self.stopAddItemSlot()
        self.cleanShape()
        self.dataListWidget.setCurrentItem(
            self.dataListWidget.itemBelow(self.dataListWidget.currentItem()))

    def treeCurrentItemChangedSlot(self, curren_item, previ_item):
        if curren_item is None:
            self.dataListWidget.setCurrentItem(previ_item)
            return
        if curren_item.text(0).find(SEPARATE_FLAG) != -1:
            if previ_item != self.dataListWidget.itemBelow(curren_item):
                self.dataListWidget.setCurrentItem(
                    self.dataListWidget.itemBelow(curren_item))
            else:
                self.dataListWidget.setCurrentItem(
                    self.dataListWidget.itemAbove(curren_item))
        else:
            # 若当前文件是待标注文件
            self.cleanShape()
            self.current_t_path = os.path.join(
                self.data_dir,
                *curren_item.parent().text(0).split(SEPARATE_FLAG))
            self.current_s_path = os.path.join(
                self.data_dir,
                curren_item.parent().text(0).split(SEPARATE_FLAG)[0],
                curren_item.text(0))
            self.current_t_qimage=toQImage(self.current_t_path)
            self.tem_draw_area.loadPixmap(
                QPixmap.fromImage(self.current_t_qimage))
            self.current_s_qimage=toQImage(self.current_s_path)
            self.sample_draw_area.loadPixmap(
                QPixmap.fromImage(self.current_s_qimage))

            labelfile = os.path.splitext(self.current_s_path)[0] + '.json'
            if os.path.exists(labelfile):
                with open(labelfile, 'r') as fr:
                    content = json.load(fr)

                self.tem_draw_area.scene().add_points(
                    content['Template']['Points'])
                self.sample_draw_area.scene().add_points(
                    content['Sample']['Points'])

                for idx, (titem, sitem) in enumerate(
                        zip(self.tem_draw_area.scene().items(),
                            self.sample_draw_area.scene().items())):
                    self.shapes_info[titem.hash][
                        'TemplateShape'] = self.tem_draw_area.scene().items(
                        )[idx]
                    self.shapes_info[sitem.hash][
                        'SampleShape'] = self.sample_draw_area.scene().items(
                        )[idx]

                    listItem = LabelListItem(text=str(titem._label),
                                             hash=titem.hash,
                                             parent=self.labelListWidget)
                    self.labelListWidget.addItem(listItem)
                    self.shapes_info[titem.hash]['ListItem'] = listItem
                H=np.array(content["Sample2Template Matrix"])
                print(H)
                self.checkDockWidgetView.showFinalImage(self.current_t_qimage,self.current_s_qimage,H.T)

                self.stopAddItemSlot()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())