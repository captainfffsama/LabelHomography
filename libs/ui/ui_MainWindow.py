# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chiebotgpuhq/MyCode/python/labelP/labelp/libs/ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(746, 801)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/futurama.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 746, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuChange_Shape = QtWidgets.QMenu(self.menuEdit)
        self.menuChange_Shape.setObjectName("menuChange_Shape")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setMinimumSize(QtCore.QSize(0, 0))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setIconSize(QtCore.QSize(48, 48))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.dockWidget_file = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_file.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dockWidget_file.setAutoFillBackground(True)
        self.dockWidget_file.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_file.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_file.setObjectName("dockWidget_file")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dataListWidget = QtWidgets.QTreeWidget(self.dockWidgetContents_3)
        self.dataListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dataListWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.dataListWidget.setLineWidth(0)
        self.dataListWidget.setAutoScrollMargin(2)
        self.dataListWidget.setHeaderHidden(True)
        self.dataListWidget.setObjectName("dataListWidget")
        self.dataListWidget.headerItem().setText(0, "1")
        self.horizontalLayout_2.addWidget(self.dataListWidget)
        self.dockWidget_file.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_file)
        self.dockWidget_label = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_label.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_label.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_label.setObjectName("dockWidget_label")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelListWidget = QtWidgets.QListWidget(self.dockWidgetContents_4)
        self.labelListWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.labelListWidget.setObjectName("labelListWidget")
        self.horizontalLayout_3.addWidget(self.labelListWidget)
        self.dockWidget_label.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_label)
        self.actionOpenDir = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenDir.setIcon(icon1)
        self.actionOpenDir.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionOpenDir.setObjectName("actionOpenDir")
        self.actionPreviousSample = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icon/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreviousSample.setIcon(icon2)
        self.actionPreviousSample.setObjectName("actionPreviousSample")
        self.actionNextSample = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icon/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNextSample.setIcon(icon3)
        self.actionNextSample.setObjectName("actionNextSample")
        self.actionAddShape = QtWidgets.QAction(MainWindow)
        self.actionAddShape.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icon/add-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddShape.setIcon(icon4)
        self.actionAddShape.setObjectName("actionAddShape")
        self.actionPoint_Shape = QtWidgets.QAction(MainWindow)
        self.actionPoint_Shape.setCheckable(True)
        self.actionPoint_Shape.setChecked(True)
        self.actionPoint_Shape.setAutoRepeat(False)
        self.actionPoint_Shape.setObjectName("actionPoint_Shape")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/icon/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon5)
        self.actionSave.setObjectName("actionSave")
        self.actionAuto_Save = QtWidgets.QAction(MainWindow)
        self.actionAuto_Save.setCheckable(True)
        self.actionAuto_Save.setObjectName("actionAuto_Save")
        self.menuFile.addAction(self.actionOpenDir)
        self.menuFile.addAction(self.actionSave)
        self.menuChange_Shape.addAction(self.actionPoint_Shape)
        self.menuEdit.addAction(self.menuChange_Shape.menuAction())
        self.menuEdit.addAction(self.actionAuto_Save)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionOpenDir)
        self.toolBar.addAction(self.actionPreviousSample)
        self.toolBar.addAction(self.actionNextSample)
        self.toolBar.addAction(self.actionAddShape)
        self.toolBar.addAction(self.actionSave)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Label Homography"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuChange_Shape.setTitle(_translate("MainWindow", "Change Shape"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_file.setWindowTitle(_translate("MainWindow", "Data List"))
        self.dockWidget_label.setWindowTitle(_translate("MainWindow", "Label List"))
        self.labelListWidget.setSortingEnabled(True)
        self.actionOpenDir.setText(_translate("MainWindow", "Open Dir"))
        self.actionPreviousSample.setText(_translate("MainWindow", "Previous Sample"))
        self.actionPreviousSample.setToolTip(_translate("MainWindow", "Previous Sample"))
        self.actionPreviousSample.setShortcut(_translate("MainWindow", "A"))
        self.actionNextSample.setText(_translate("MainWindow", "Next Sample"))
        self.actionNextSample.setShortcut(_translate("MainWindow", "D"))
        self.actionAddShape.setText(_translate("MainWindow", "Add Shape"))
        self.actionAddShape.setToolTip(_translate("MainWindow", "Add Shape"))
        self.actionAddShape.setShortcut(_translate("MainWindow", "W"))
        self.actionPoint_Shape.setText(_translate("MainWindow", "Point Shape"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionAuto_Save.setText(_translate("MainWindow", "Auto Save"))
import apprcc_rc
