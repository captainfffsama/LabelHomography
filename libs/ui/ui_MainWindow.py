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
        MainWindow.resize(817, 801)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuview = QtWidgets.QMenu(self.menubar)
        self.menuview.setObjectName("menuview")
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
        self.toolBar.setMinimumSize(QtCore.QSize(50, 0))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.dockWidget_label = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dockWidget_label.setAutoFillBackground(True)
        self.dockWidget_label.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_label.setObjectName("dockWidget_label")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.dockWidgetContents_3)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.treeWidget.setLineWidth(0)
        self.treeWidget.setAutoScrollMargin(2)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.dockWidget_label.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_label)
        self.dockWidget_file = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_file.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_file.setObjectName("dockWidget_file")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget = QtWidgets.QListWidget(self.dockWidgetContents_4)
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_3.addWidget(self.listWidget)
        self.dockWidget_file.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_file)
        self.actionOpen_Dir = QtWidgets.QAction(MainWindow)
        self.actionOpen_Dir.setObjectName("actionOpen_Dir")
        self.actionprevious_sample = QtWidgets.QAction(MainWindow)
        self.actionprevious_sample.setObjectName("actionprevious_sample")
        self.actionnext_sample = QtWidgets.QAction(MainWindow)
        self.actionnext_sample.setObjectName("actionnext_sample")
        self.menuFile.addAction(self.actionOpen_Dir)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuview.menuAction())
        self.toolBar.addAction(self.actionOpen_Dir)
        self.toolBar.addAction(self.actionprevious_sample)
        self.toolBar.addAction(self.actionnext_sample)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "label point"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuview.setTitle(_translate("MainWindow", "view"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_label.setWindowTitle(_translate("MainWindow", "Data List"))
        self.dockWidget_file.setWindowTitle(_translate("MainWindow", "Label List"))
        self.actionOpen_Dir.setText(_translate("MainWindow", "Open Dir"))
        self.actionprevious_sample.setText(_translate("MainWindow", "previous sample"))
        self.actionnext_sample.setText(_translate("MainWindow", "next sample"))
